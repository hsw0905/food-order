import asyncio
import os

import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, async_scoped_session, AsyncConnection, \
    AsyncTransaction
from uvloop import new_event_loop

from app import create_app
from core.config import config
from core.db.sqlalchemy import Base
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
    _is_local_db_used(config.DB_URL)

    test_engine = create_async_engine(
        url=config.DB_URL,
        echo=config.DB_ECHO,
        pool_pre_ping=config.DB_PRE_PING
    )

    yield test_engine

    await test_engine.dispose()


def is_sqlite_used(database_url: str):
    if ":memory:" in database_url:
        return True
    return False


def _is_local_db_used(database_url: str):
    """
    local db를 사용하면 memory db 삭제
    """
    if ":memory:" not in database_url:
        if os.path.exists(database_url.split("sqlite:///")[-1]):  # :memory:
            os.unlink(database_url.split("sqlite:///")[-1])


@pytest_asyncio.fixture
async def test_session(test_db):
    async_session_factory: async_sessionmaker = async_sessionmaker(
        bind=test_db,
        autoflush=False,
        autocommit=False
    )

    scoped_session: async_scoped_session = async_scoped_session(
        session_factory=async_session_factory,
        scopefunc=asyncio.current_task
    )

    connection: AsyncConnection = await test_db.connect()
    transaction: AsyncTransaction = await connection.begin()

    if is_sqlite_used(config.DB_URL):
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    try:
        yield scoped_session
    except Exception as e:
        await scoped_session.rollback()
        logger.error(f"session rollback due to error: {e}")
    finally:
        await transaction.rollback()
        await connection.close()
        await scoped_session.remove()
