import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from core.domains.user.enum.user_enum import UserStatus
from core.domains.user.repository.user_repository import UserRepository
from core.persistence.models.user_model import UserModel


@pytest.mark.asyncio
async def test_should_save_user(
    test_session: async_scoped_session[AsyncSession],
) -> None:
    user_repository = UserRepository()
    test_user = UserModel(email="harry@example.com", password="1234")

    await user_repository.save(test_user)
    user = await user_repository.find_by_id(1)

    assert user is not None
    assert user.email == test_user.email
    assert user.password == test_user.password
    assert user.status == UserStatus.PENDING.value


@pytest.mark.asyncio
async def test_should_find_user_by_email(
    test_session: async_scoped_session[AsyncSession],
) -> None:
    user_repository = UserRepository()
    test_user = UserModel(email="harry@example.com", password="1234")
    await user_repository.save(test_user)

    user = await user_repository.find_by_email(test_user.email)

    assert user is not None
    assert user.email == test_user.email
    assert user.password == test_user.password
