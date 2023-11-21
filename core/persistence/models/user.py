from sqlalchemy import VARCHAR, Boolean
from sqlalchemy.orm import mapped_column

from core.domains.user.enum.user_enum import UserStatus
from core.persistence.models.base import Base
from core.persistence.models.base_time import BaseTimeEntity


class User(Base, BaseTimeEntity):
    __tablename__ = "users"

    email = mapped_column(VARCHAR(100), nullable=False)
    password = mapped_column(VARCHAR(200), nullable=False)
    status = mapped_column(
        VARCHAR(1), comment="0 보류, 1 활성화, 2 비활성화", default=UserStatus.PENDING.value
    )
    is_admin = mapped_column(Boolean, nullable=False, default=False)
