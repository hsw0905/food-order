import bcrypt


class PasswordEncoder:
    @classmethod
    def hash(cls, plain_password: str) -> str:
        return bcrypt.hashpw(plain_password.encode("UTF-8"), bcrypt.gensalt()).decode()

    @classmethod
    def verify(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("UTF-8"), hashed_password.encode("UTF-8")
        )
