from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.config import config

engine: AsyncEngine = create_async_engine(
    url=config.DB_URL, echo=config.DB_ECHO, pool_pre_ping=config.DB_PRE_PING
)

async_session_factory = async_sessionmaker(
    bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
)

session = async_scoped_session(
    session_factory=async_session_factory, scopefunc=current_task
)
