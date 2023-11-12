from sqlalchemy import select
from sqlalchemy.exc import DatabaseError
from sqlalchemy.orm import Session

from app.exceptions.base_exception import InternalServerErrorException
from app.models.user import User
from core.utils.log_helper import logger_

logger = logger_.getLogger(__name__)


class UserRepository:
    def __init__(self, session: Session):
        self._session = session

    def save(self, email: str, password: str) -> None:
        user = User(email=email, password=password)

        try:
            self._session.add(user)
            self._session.commit()
        except DatabaseError as e:
            logger.error(f"[UserRepository][save]: error: {e.detail}")
            self._session.rollback()
            raise InternalServerErrorException("서버 내부 오류")

    def find_by_id(self, user_id) -> User:
        statement = (
            select(User).where(User.id == user_id)
        )

        return self._session.execute(statement).scalar()


