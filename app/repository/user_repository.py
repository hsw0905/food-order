from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.asyncio import AsyncSession

from app.entity.user import User
from app.exception.base_exception import InternalServerErrorException
from core.util.log_helper import logger_

logger = logger_.getLogger(__name__)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, email: str, password: str) -> None:
        user = User(email=email, password=password)

        try:
            self._session.add(user)
            await self._session.commit()
        except DatabaseError as e:
            logger.error(f"[UserRepository][save]: error: {e.detail}")
            await self._session.rollback()
            raise InternalServerErrorException("서버 내부 오류")

    async def find_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)

        result = await self._session.execute(statement)

        return result.scalar()
