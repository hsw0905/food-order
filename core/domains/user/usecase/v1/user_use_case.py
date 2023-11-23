import bcrypt
import inject

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

        encrypted_password = self._encrypt_password(dto.password)
        await self._create_user(dto.email, encrypted_password)

    async def _create_user(self, email: str, password: str) -> None:
        user = UserModel(email=email, password=password)
        await self._user_repo.save(user)

    def _encrypt_password(self, password: str) -> str:
        to_encrypt: bytes = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())

        return to_encrypt.decode()
