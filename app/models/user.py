from sqlalchemy import Column, BigInteger, Integer, String, Boolean

from core.db.mixins import TimestampMixin
from core.db.sqlalchemy import Base


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(
        BigInteger().with_variant(Integer, "sqlite"),
        primary_key=True,
        nullable=False
    )
    email = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)

