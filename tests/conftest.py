import pytest
from fastapi import FastAPI
from sqlalchemy import Engine, create_engine, Connection, Transaction
from sqlalchemy.orm import sessionmaker

from app import create_app
from core.config import TestConfig
from core.db.sqlalchemy import Base


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest.fixture
def test_db():
    test_config = TestConfig()

    test_engine: Engine = create_engine(
        url=test_config.DB_URL,
        echo=test_config.DB_ECHO,
        pool_pre_ping=test_config.DB_PRE_PING,
        connect_args={"check_same_thread": False}
    )

    yield test_engine

    test_engine.dispose()


@pytest.fixture
def test_session(test_db):
    session_factory = sessionmaker(bind=test_db, autoflush=False, autocommit=False)

    connection: Connection = test_db.connect()
    transaction: Transaction = connection.begin()

    Base.metadata.drop_all(connection)
    Base.metadata.create_all(connection)

    with session_factory() as session:
        yield session

    transaction.rollback()
    connection.close()
