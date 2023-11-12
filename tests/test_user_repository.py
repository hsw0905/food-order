from app.repositories.user_repository import UserRepository


def test_save(test_session):
    user_repository = UserRepository(test_session)
    test_email = "harry@example.com"
    test_password = "1234"
    user_repository.save(test_email, test_password)

    user = user_repository.find_by_id(1)

    assert user.email == test_email
    assert user.password == test_password
