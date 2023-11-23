from app.exceptions.base_exception import InvalidRequestException


class DuplicatedUserException(InvalidRequestException):
    def __init__(self) -> None:
        super().__init__("이미 가입된 사용자입니다.")
