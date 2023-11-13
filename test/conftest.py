from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    AsyncTransaction,
    async_sessionmaker,
    create_async_engine,
)
from uvloop import Loop, new_event_loop

from app import create_app
from app.entity.base_entity import Base
from core.config import config


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture(scope="session")
async def running_app(app: FastAPI) -> AsyncGenerator[FastAPI, None]:
    async with LifespanManager(app=app):
        yield app


@pytest.fixture(scope="session")
def event_loop() -> Generator[Loop, None, None]:
    """pytest->event_loop fixture를 override 하기 위한 코드"""
    loop = new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_client(running_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=running_app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def test_db() -> AsyncGenerator[AsyncEngine, None]:
    test_engine: AsyncEngine = create_async_engine(
        url=config.DB_URL,
        echo=config.DB_ECHO,
        pool_pre_ping=config.DB_PRE_PING,
    )

    yield test_engine

    await test_engine.dispose()


@pytest.fixture
def test_session_factory(
    test_db: AsyncEngine,
) -> Generator[async_sessionmaker[AsyncSession], None, None]:
    session_factory = async_sessionmaker(
        bind=test_db, autoflush=False, autocommit=False
    )
    yield session_factory


@pytest_asyncio.fixture
async def test_session(
    test_db: AsyncEngine, test_session_factory: async_sessionmaker[AsyncSession]
) -> AsyncGenerator[AsyncSession, None]:
    connection: AsyncConnection = await test_db.connect()
    transaction: AsyncTransaction = await connection.begin()

    await connection.run_sync(Base.metadata.drop_all)
    await connection.run_sync(Base.metadata.create_all)

    async with test_session_factory() as session:
        yield session

    await transaction.rollback()
    await connection.close()
