from sqlalchemy import Boolean, String
from sqlalchemy.orm import mapped_column

from app.common.entity.base_entity import Base
from app.common.entity.base_time_entity import BaseTimeEntity


class User(Base, BaseTimeEntity):
    __tablename__ = "users"

    email = mapped_column(String(100), nullable=False)
    password = mapped_column(String(100), nullable=False)
    is_active = mapped_column(Boolean, nullable=False, default=False)
    is_admin = mapped_column(Boolean, nullable=False, default=False)
