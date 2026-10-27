# ADR 0001: One role-to-permission map

## Problem

The template treated authorization as a boolean, `is_superuser`. The assignment needs three roles, and the same decision has to be enforced on the API and in the UI. Spreading `if role == ...` through every route would make the next role a wide edit, and a separate policy engine would be more machinery than this surface needs.

## Options

1. Keep `is_superuser` and add more booleans, such as `is_manager`. Each check still names a flag, and the flags can disagree.
2. Store roles and permissions in tables and resolve them per request. That fits a product where admins edit grants in the UI. It is a second model, more queries, and more tests than this task asks for.
3. Store one `role` string on the user and keep a dictionary from role to permissions in one module. Routes name a permission. The UI reads the permission list from `GET /users/me` instead of copying the dictionary.

## Decision

Option 3. `Role` and `Permission` live in `backend/app/core/authorization.py`. `require_permission` is the only FastAPI dependency that answers "may this caller do this?". Signup cannot set a role; it always creates a `member`. An admin assigns roles through the user-management endpoints. Own-profile updates do not accept a role, so a member cannot promote themselves.

The column is a varchar, not a Postgres enum. Adding a value does not need a database enum migration. The trade-off is that the database will not reject an unknown string by itself; the application validates the role on write.

The frontend trusts the `permissions` array on the current user for navigation and for hiding buttons. That can drift only if the API lies. Direct URLs still hit the same dependency, so hiding a link is not the security boundary.

## Consequences

A new role is one entry in `ROLE_PERMISSIONS`, plus the place that assigns it. Denied calls are logged with the user id and the permission name. We did not build an admin screen for editing the matrix, and we did not add per-user exceptions. If those show up later, the route dependencies can stay; only the map's source would change.
