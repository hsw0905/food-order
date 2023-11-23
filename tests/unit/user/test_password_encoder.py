from app.utils.password_encoder import PasswordEncoder


def test_should_match_password() -> None:
    test_password = "1234"
    hashed = PasswordEncoder.hash(test_password)

    assert PasswordEncoder.verify(test_password, hashed) is True
