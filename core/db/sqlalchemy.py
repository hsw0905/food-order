import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, async_scoped_session, \
    AsyncSession
from sqlalchemy.orm import declarative_base, DeclarativeMeta

from core.config import config

engine: AsyncEngine = create_async_engine(
    url=config.DB_URL,
    echo=config.DB_ECHO,
    pool_pre_ping=config.DB_PRE_PING
)

session: async_scoped_session[AsyncSession] = async_scoped_session(
    session_factory=async_sessionmaker(bind=engine, autoflush=False, autocommit=False),
    scopefunc=asyncio.current_task
)

Base: DeclarativeMeta = declarative_base()
