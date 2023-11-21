"""add status user model

Revision ID: 1383214c2653
Revises: e728fbd84412
Create Date: 2023-11-20 16:52:31.638739

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from core.domains.user.enum.user_enum import UserStatus

# revision identifiers, used by Alembic.
revision: str = "1383214c2653"
down_revision: Union[str, None] = "e728fbd84412"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "id",
        existing_type=sa.BigInteger,
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )

    op.drop_column("users", "is_active")

    op.add_column(
        "users",
        sa.Column(
            "status",
            sa.Enum(UserStatus),
            nullable=False,
            default=UserStatus.PENDING.value,
        ),
    )


def downgrade() -> None:
    op.alter_column(
        "users", "id", existing_type=sa.BigInteger, nullable=False, primary_key=True
    )

    op.drop_column("users", "status")

    op.add_column(
        "users", sa.Column("is_active", sa.Boolean, nullable=False, default=False)
    )
