from sqlalchemy import select
from sqlalchemy.exc import DatabaseError

from app.entity.user import User
from core.database.sqlalchemy import session
from core.exception.base_exception import InternalServerErrorException
from core.util.log_helper import logger_

logger = logger_.getLogger(__name__)


class UserRepository:
    async def save(self, email: str, password: str) -> None:
        user = User(email=email, password=password)

        try:
            session.add(user)
            await session.commit()
        except DatabaseError as e:
            logger.error(f"[UserRepository][save]: error: {e.detail}")
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
