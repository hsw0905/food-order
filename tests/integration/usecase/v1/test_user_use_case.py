import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from core.domains.user.exception.user_exception import DuplicatedUserException
from core.domains.user.repository.user_repository import UserRepository
from core.domains.user.usecase.v1.dto.user_dto import SignUpDto
from core.domains.user.usecase.v1.user_use_case import SignUpUseCase
from core.persistence.models.user_model import UserModel


@pytest.mark.asyncio
async def test_should_raise_duplicated_user_exception(
    test_session: async_scoped_session[AsyncSession],
) -> None:
    user_repo = UserRepository()
    use_case = SignUpUseCase()

    test_email = "harry@example.com"
    test_password = "1234"

    dto = SignUpDto(email=test_email, password=test_password)

    test_user = UserModel(email=test_email, password=test_password)
    await user_repo.save(test_user)

    with pytest.raises(DuplicatedUserException):
        await use_case.execute(dto)
