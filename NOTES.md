# Notes

The implementation covers the permission matrix, backend enforcement, the matching UI, focused API tests, and the setup steps in the README.

Left out on purpose:

- Playwright coverage. The template already has end-to-end tests, and the assignment asked for a few backend authorization tests rather than a full UI suite.
- A roles or permissions table. Roles are a single column and a dictionary. An admin cannot edit the matrix from the UI.
- A separate global-settings screen. The template does not have one. "Manager cannot change global settings" means a manager cannot create users, change roles, or call the old superuser utilities such as the test-email endpoint.
- Renaming `FIRST_SUPERUSER`. That env var still seeds the admin so the existing Docker Compose files keep working.

With more time I would generate the frontend client from the OpenAPI schema instead of editing the committed types by hand, and I would add a short audit view of denied requests beyond the log line.
