from inject import Binder, clear_and_configure

from app.repository.user_repository import UserRepository
from core.db.sqlalchemy import async_session_factory


def configure_app(binder: Binder) -> None:
    binder.bind(UserRepository, UserRepository(session=async_session_factory()))


def init_provider() -> None:
    clear_and_configure(configure_app)
