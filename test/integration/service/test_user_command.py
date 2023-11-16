import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.user.dto.v1.request.user_request import CreateUserDto
from app.user.repository.user_repository import UserRepository
from app.user.service.v1.user_service import CreateUserService
from core.exception.base_exception import InvalidRequestException


@pytest.mark.asyncio
async def test_should_raise_exception_when_duplicated_email(
    test_session: async_scoped_session[AsyncSession],
) -> None:
    user_repository = UserRepository()
    user_command = CreateUserService()

    dto = CreateUserDto(email="harry@example.com", password="1234")
    await user_repository.save(dto.email, dto.password)

    with pytest.raises(InvalidRequestException):
        await user_command.execute(dto)
