import inject

from app.utils.password_encoder import PasswordEncoder
from core.domains.user.exception.user_exception import DuplicatedUserException
from core.domains.user.repository.user_repository import UserRepository
from core.domains.user.usecase.v1.dto.user_dto import SignUpDto
from core.persistence.models.user_model import UserModel


class SignUpUseCase:
    @inject.autoparams()
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def execute(self, dto: SignUpDto) -> None:
        duplicated_user = await self._user_repo.find_by_email(dto.email)
        if duplicated_user:
            raise DuplicatedUserException

        hashed_password = PasswordEncoder.hash(dto.password)
        await self._create_user(dto.email, hashed_password)

    async def _create_user(self, email: str, hashed_password: str) -> None:
        user = UserModel(email=email, password=hashed_password)
        await self._user_repo.save(user)
