import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.user.repository.user_repository import UserRepository


@pytest.mark.asyncio
async def test_should_save_users(
    test_session: async_scoped_session[AsyncSession],
) -> None:
    user_repository = UserRepository()
    test_email = "harry@example.com"
    test_password = "1234"

    await user_repository.save(test_email, test_password)

    user = await user_repository.find_by_id(1)

    assert user is not None
    assert user.email == test_email
    assert user.password == test_password


@pytest.mark.asyncio
async def test_find_by_email(test_session: async_scoped_session[AsyncSession]) -> None:
    user_repository = UserRepository()
    test_email = "harry@example.com"
    test_password = "1234"

    await user_repository.save(test_email, test_password)

    user = await user_repository.find_by_email(test_email)

    assert user is not None
    assert user.email == test_email
    assert user.password == test_password
