import inject

from app.user.dto.v1.request.user_request import CreateUserDto
from app.user.repository.user_repository import UserRepository
from core.exception.base_exception import InvalidRequestException


class CreateUserService:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, dto: CreateUserDto) -> None:
        duplicated_user = await self._user_repo.find_by_email(dto.email)

        if duplicated_user:
            raise InvalidRequestException("Already Exists Email")
