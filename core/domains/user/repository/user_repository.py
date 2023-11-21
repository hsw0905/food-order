from sqlalchemy import select
from sqlalchemy.exc import DatabaseError

from app.database.sqlalchemy import session
from app.exceptions.base_exception import InternalServerErrorException
from app.utils.log_helper import logger_
from core.persistence.models.user import User

logger = logger_.getLogger(__name__)


class UserRepository:
    async def save(self, user: User) -> None:
        try:
            session.add(user)
            await session.commit()
        except DatabaseError as e:
            logger.error(f"[UserRepository][save]: {e.detail}")
            await session.rollback()
            raise InternalServerErrorException("서버 내부 오류")

    async def find_by_id(self, user_id: int) -> User | None:
        statement = select(User).where(User.id == user_id)

        result = await session.execute(statement)

        return result.scalar()

    async def find_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)

        result = await session.execute(statement)

        return result.scalar()
