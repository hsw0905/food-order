from sqlalchemy import select
from sqlalchemy.exc import DatabaseError

from app.database.sqlalchemy import session
from app.exceptions.base_exception import InternalServerErrorException
from app.utils.log_helper import logger_
from core.domains.user.entity.user_entity import UserEntity
from core.persistence.models.user_model import UserModel

logger = logger_.getLogger(__name__)


class UserRepository:
    async def save(self, user: UserModel) -> None:
        try:
            session.add(user)
            await session.commit()
        except DatabaseError as e:
            logger.error(f"[UserRepository][save]: {e.detail}")
            await session.rollback()
            raise InternalServerErrorException("서버 내부 오류")

    async def find_by_id(self, user_id: int) -> UserEntity | None:
        statement = select(UserModel).where(UserModel.id == user_id)

        result = await session.execute(statement)

        row = result.scalar()

        if not row:
            return None
        return row.to_entity()

    async def find_by_email(self, email: str) -> UserEntity | None:
        statement = select(UserModel).where(UserModel.email == email)

        result = await session.execute(statement)

        row = result.scalar()

        if not row:
            return None
        return row.to_entity()
