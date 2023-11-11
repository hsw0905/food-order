from sqlalchemy import select
from sqlalchemy.exc import DatabaseError

from app.exceptions.base_exception import InternalServerErrorException
from app.models.user import User
from core.db.sqlalchemy import session
from core.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class UserRepository:
    async def save(self, email: str, password: str):
        user = User(email=email, password=password)

        try:
            session.add(user)
            await session.commit()
        except DatabaseError as e:
            logger.error(f"[UserRepository][save]: error: {e.detail}")
            await session.rollback()
            raise InternalServerErrorException("서버 내부 오류")

    async def find_by_id(self, user_id):
        statement = (
            select(User).where(User.id == user_id)
        )

        return await session.execute(statement)

