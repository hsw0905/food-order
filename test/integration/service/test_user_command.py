import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.controller.dto.request.user_request import CreateUserDto
from app.repository.user_repository import UserRepository
from app.service.user.user_command import CreateUserCommand
from core.exception.base_exception import InvalidRequestException


@pytest.mark.asyncio
async def test_should_raise_exception_when_duplicated_email(
    test_session: async_scoped_session[AsyncSession],
) -> None:
    user_repository = UserRepository()
    user_command = CreateUserCommand()

    dto = CreateUserDto(email="harry@example.com", password="1234")
    await user_repository.save(dto.email, dto.password)

    with pytest.raises(InvalidRequestException):
        await user_command.execute(dto)
