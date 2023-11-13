from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


def test_should_different_session(
    test_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    session_1 = test_session_factory()
    session_2 = test_session_factory()

    assert session_1 != session_2
