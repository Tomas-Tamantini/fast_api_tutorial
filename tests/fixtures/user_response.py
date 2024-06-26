import pytest


@pytest.fixture
def user_response():
    def _user_response(
        id: int = 1,
        username: str = "test",
        email: str = "a@b.com",
        password: str = "123",
    ) -> dict:
        return {"id": id, "username": username, "email": email, "password": password}

    return _user_response
