from fastapi.testclient import TestClient
from sqlmodel import Session

from app import crud
from app.core.authorization import Role
from app.core.config import settings
from app.models import UserCreate
from tests.utils.user import user_authentication_headers
from tests.utils.utils import random_email, random_lower_string


def _headers_for_role(*, client: TestClient, db: Session, role: Role) -> dict[str, str]:
    email = random_email()
    password = random_lower_string()
    crud.create_user(
        session=db,
        user_create=UserCreate(email=email, password=password, role=role),
    )
    return user_authentication_headers(client=client, email=email, password=password)


def test_member_cannot_list_users(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/users/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Access denied"}


def test_manager_can_list_users_but_cannot_create_user(
    client: TestClient, db: Session
) -> None:
    headers = _headers_for_role(client=client, db=db, role=Role.MANAGER)

    listed = client.get(f"{settings.API_V1_STR}/users/", headers=headers)
    assert listed.status_code == 200
    assert "data" in listed.json()

    created = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=headers,
        json={"email": random_email(), "password": random_lower_string()},
    )
    assert created.status_code == 403
    assert created.json() == {"detail": "Access denied"}


def test_admin_can_create_user(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        headers=superuser_token_headers,
        json={"email": random_email(), "password": random_lower_string()},
    )
    assert response.status_code == 200
    assert response.json()["role"] == Role.MEMBER


def test_metrics_are_visible_to_manager_and_hidden_from_member(
    client: TestClient, db: Session, normal_user_token_headers: dict[str, str]
) -> None:
    denied = client.get(
        f"{settings.API_V1_STR}/metrics/",
        headers=normal_user_token_headers,
    )
    assert denied.status_code == 403
    assert denied.json() == {"detail": "Access denied"}

    headers = _headers_for_role(client=client, db=db, role=Role.MANAGER)
    allowed = client.get(f"{settings.API_V1_STR}/metrics/", headers=headers)
    assert allowed.status_code == 200
    body = allowed.json()
    assert body["user_count"] >= 1
    assert set(body["users_by_role"]) == {"admin", "manager", "member"}


def test_member_can_update_own_profile_but_not_another(
    client: TestClient, db: Session, normal_user_token_headers: dict[str, str]
) -> None:
    other = crud.create_user(
        session=db,
        user_create=UserCreate(
            email=random_email(), password=random_lower_string(), role=Role.MEMBER
        ),
    )

    own = client.patch(
        f"{settings.API_V1_STR}/users/me",
        headers=normal_user_token_headers,
        json={"full_name": "Member Name"},
    )
    assert own.status_code == 200
    assert own.json()["full_name"] == "Member Name"
    assert own.json()["role"] == Role.MEMBER

    foreign = client.patch(
        f"{settings.API_V1_STR}/users/{other.id}",
        headers=normal_user_token_headers,
        json={"full_name": "Taken Over"},
    )
    assert foreign.status_code == 403
    assert foreign.json() == {"detail": "Access denied"}


def test_signup_cannot_choose_a_role(client: TestClient) -> None:
    response = client.post(
        f"{settings.API_V1_STR}/users/signup",
        json={
            "email": random_email(),
            "password": random_lower_string(),
            "role": Role.ADMIN,
        },
    )
    assert response.status_code == 200
    assert response.json()["role"] == Role.MEMBER
