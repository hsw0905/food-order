from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import async_scoped_session

from app.exceptions.base_exception import InternalServerErrorException
from app.models.user import User
from core.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class UserRepository:
    def __init__(self, async_session: async_scoped_session):
        self._session = async_session

    async def save(self, email: str, password: str) -> None:
        user = User(email=email, password=password)

        try:
            self._session.add(user)
            await self._session.commit()
        except DatabaseError as e:
            logger.error(f"[UserRepository][save]: error: {e.detail}")
            await self._session.rollback()
            raise InternalServerErrorException("서버 내부 오류")

    async def find_by_id(self, user_id):
        statement = (
            select(User).where(User.id == user_id)
        )

        result = await self._session.execute(statement)

        return result.scalar()
