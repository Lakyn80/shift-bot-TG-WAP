"""add password_hash to users

Revision ID: 22e8527a879c
Revises: abdf447b8d99
Create Date: 2026-01-01 16:52:44.828901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22e8527a879c'
down_revision: Union[str, Sequence[str], None] = 'abdf447b8d99'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("password_hash", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "password_hash")
