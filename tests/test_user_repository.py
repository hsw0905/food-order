import pytest

from app.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_save(test_session):
    user_repository = UserRepository(test_session)
    test_email = "harry@example.com"
    test_password = "1234"
    await user_repository.save(test_email, test_password)

    user = await user_repository.find_by_id(1)

    assert user.email == test_email
    assert user.password == test_password
