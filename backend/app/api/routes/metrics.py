from fastapi import APIRouter, Depends
from sqlmodel import func, select

from app.api.deps import SessionDep, require_permission
from app.core.authorization import Permission, Role
from app.models import MetricsPublic, User

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get(
    "/",
    dependencies=[Depends(require_permission(Permission.METRICS_VIEW))],
    response_model=MetricsPublic,
)
def read_metrics(session: SessionDep) -> MetricsPublic:
    """
    User counts grouped by role.
    """
    rows = session.exec(select(User.role, func.count()).group_by(User.role)).all()
    users_by_role = {role.value: 0 for role in Role}
    for role, count in rows:
        users_by_role[Role(role).value] = count
    return MetricsPublic(
        user_count=sum(users_by_role.values()),
        users_by_role=users_by_role,
    )
