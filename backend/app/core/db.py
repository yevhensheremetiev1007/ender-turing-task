from sqlmodel import Session, create_engine, select

from app import crud
from app.core.authorization import Role
from app.core.config import settings
from app.models import User, UserCreate

engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/fastapi/full-stack-fastapi-template/issues/28


def _ensure_user(session: Session, *, email: str, password: str, role: Role) -> None:
    user = session.exec(select(User).where(User.email == email)).first()
    if user:
        return
    crud.create_user(
        session=session,
        user_create=UserCreate(email=email, password=password, role=role),
    )


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    _ensure_user(
        session,
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        role=Role.ADMIN,
    )
    _ensure_user(
        session,
        email=settings.FIRST_MANAGER,
        password=settings.FIRST_MANAGER_PASSWORD,
        role=Role.MANAGER,
    )
    _ensure_user(
        session,
        email=settings.FIRST_MEMBER,
        password=settings.FIRST_MEMBER_PASSWORD,
        role=Role.MEMBER,
    )
