"""Role to permission map.

Route dependencies ask for a permission. Adding a role means adding one entry
in ROLE_PERMISSIONS, not another scattered check.
"""

from enum import StrEnum


class Role(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    MEMBER = "member"


class Permission(StrEnum):
    USERS_LIST = "users:list"
    USERS_CREATE = "users:create"
    USERS_READ_ANY = "users:read_any"
    USERS_UPDATE_ANY = "users:update_any"
    USERS_DELETE_ANY = "users:delete_any"
    METRICS_VIEW = "metrics:view"
    ITEMS_READ_ALL = "items:read_all"
    SETTINGS_MANAGE = "settings:manage"


ACCESS_DENIED_DETAIL = "Access denied"

_MANAGER_PERMISSIONS = frozenset(
    {
        Permission.USERS_LIST,
        Permission.USERS_READ_ANY,
        Permission.METRICS_VIEW,
    }
)
_ADMIN_PERMISSIONS = _MANAGER_PERMISSIONS | frozenset(
    {
        Permission.USERS_CREATE,
        Permission.USERS_UPDATE_ANY,
        Permission.USERS_DELETE_ANY,
        Permission.ITEMS_READ_ALL,
        Permission.SETTINGS_MANAGE,
    }
)

ROLE_PERMISSIONS: dict[Role, frozenset[Permission]] = {
    Role.MEMBER: frozenset(),
    Role.MANAGER: _MANAGER_PERMISSIONS,
    Role.ADMIN: _ADMIN_PERMISSIONS,
}


def role_has_permission(role: Role | str, permission: Permission) -> bool:
    return permission in ROLE_PERMISSIONS[Role(role)]


def permissions_for(role: Role | str) -> list[str]:
    granted = ROLE_PERMISSIONS[Role(role)]
    return sorted(permission.value for permission in granted)
