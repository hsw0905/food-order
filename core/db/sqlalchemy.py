from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import declarative_base, DeclarativeMeta, sessionmaker

from core.config import config

engine: Engine = create_engine(
    url=config.DB_URL,
    echo=config.DB_ECHO,
    pool_pre_ping=config.DB_PRE_PING
)

session_factory = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base: DeclarativeMeta = declarative_base()
