"""modify user model

Revision ID: 5324b9e69210
Revises: 1383214c2653
Create Date: 2023-11-21 13:36:08.487071

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from core.domains.user.enum.user_enum import UserStatus

# revision identifiers, used by Alembic.
revision: str = "5324b9e69210"
down_revision: Union[str, None] = "1383214c2653"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "users",
        "status",
        existing_type=sa.VARCHAR(1),
        nullable=False,
        default=UserStatus.PENDING.value,
        comment="0 보류, 1 활성화, 2 비활성화",
    )

    op.alter_column(
        "users",
        "email",
        existing_type=sa.VARCHAR(100),
        nullable=False,
        default=UserStatus.PENDING.value,
    )

    op.alter_column(
        "users",
        "password",
        existing_type=sa.VARCHAR(200),
        nullable=False,
        default=UserStatus.PENDING.value,
    )


def downgrade() -> None:
    op.alter_column(
        "users",
        "status",
        existing_type=sa.Enum(UserStatus),
        nullable=False,
        default=UserStatus.PENDING.value,
    )
