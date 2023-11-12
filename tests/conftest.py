import asyncio
import os

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncConnection, \
    AsyncTransaction, AsyncEngine, create_async_engine, async_scoped_session, async_sessionmaker, AsyncSession
from uvloop import new_event_loop

from app import create_app
from core.config import config, TestConfig
from core.db.sqlalchemy import Base, engine, session
from core.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture(scope="session")
async def running_app(app):
    async with LifespanManager(app=app):
        yield app


@pytest.fixture(scope="session")
def event_loop():
    """pytest->event_loop fixture를 override 하기 위한 코드"""
    loop = new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def async_client(running_app) -> AsyncClient:
    async with AsyncClient(app=running_app, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def test_db():
    test_config = TestConfig()

    test_engine: AsyncEngine = create_async_engine(
        url=test_config.DB_URL,
        echo=test_config.DB_ECHO,
        pool_pre_ping=test_config.DB_PRE_PING
    )

    yield test_engine

    await test_engine.dispose()


@pytest_asyncio.fixture
async def test_session(test_db):
    test_session: async_scoped_session[AsyncSession] = async_scoped_session(
        session_factory=async_sessionmaker(bind=test_db, autoflush=False, autocommit=False, expire_on_commit=False),
        scopefunc=asyncio.current_task
    )

    connection: AsyncConnection = await test_db.connect()
    transaction: AsyncTransaction = await connection.begin()

    await connection.run_sync(Base.metadata.drop_all)
    await connection.run_sync(Base.metadata.create_all)

    try:
        yield test_session
    except Exception as e:
        logger.error(f"session rollback due to error: {e}")
    finally:
        await transaction.rollback()
        await connection.close()
        await test_session.remove()
