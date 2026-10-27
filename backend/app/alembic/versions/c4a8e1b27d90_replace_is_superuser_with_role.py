"""Replace is_superuser with role

Revision ID: c4a8e1b27d90
Revises: fe56fa70289e
Create Date: 2026-10-27 17:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c4a8e1b27d90"
down_revision = "fe56fa70289e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "user",
        sa.Column(
            "role",
            sa.String(length=32),
            nullable=False,
            server_default=sa.text("'member'"),
        ),
    )
    op.execute("UPDATE \"user\" SET role = 'admin' WHERE is_superuser IS TRUE")
    op.drop_column("user", "is_superuser")


def downgrade():
    op.add_column(
        "user",
        sa.Column(
            "is_superuser",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )
    op.execute("UPDATE \"user\" SET is_superuser = TRUE WHERE role = 'admin'")
    op.drop_column("user", "role")
