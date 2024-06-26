import pytest


@pytest.fixture
def user_request():
    def _create_user_request(is_valid: bool = True) -> dict:
        return {
            "username": "test",
            "email": "valid@valid.com" if is_valid else "invalid email",
            "password": "password",
        }

    return _create_user_request
