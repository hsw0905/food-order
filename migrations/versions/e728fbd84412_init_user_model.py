"""init user model

Revision ID: 9dceb004e01b
Revises:
Create Date: 2023-11-10 18:21:26.267357

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func

# revision identifiers, used by Alembic.
revision: str = 'e728fbd84412'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.BigInteger, nullable=False, primary_key=True),
                    sa.Column("email", sa.String(100), nullable=False),
                    sa.Column("password", sa.String(100), nullable=False),
                    sa.Column("is_active", sa.Boolean, nullable=False, default=False),
                    sa.Column("is_admin", sa.Boolean, nullable=False, default=False),
                    sa.Column("created_at", sa.DateTime, nullable=False, default=func.now()),
                    sa.Column("updated_at", sa.DateTime, nullable=False, default=func.now())
                    )


def downgrade() -> None:
    op.drop_table("users")
