import inject

from app.controller.dto.request.user_request import CreateUserDto
from core.exception.base_exception import InvalidRequestException
from app.repository.user_repository import UserRepository


class CreateUserCommand:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository) -> None:
        self._user_repo = user_repo

    async def execute(self, dto: CreateUserDto) -> None:
        duplicated_user = await self._user_repo.find_by_email(dto.email)

        if duplicated_user:
            raise InvalidRequestException("Already Exists Email")
