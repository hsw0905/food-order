from datetime import datetime

from pydantic import BaseModel


class UserEntity(BaseModel):
    id: int
    email: str
    password: str
    status: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime
