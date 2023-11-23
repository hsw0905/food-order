from pydantic import BaseModel


class SignUpDto(BaseModel):
    email: str
    password: str
