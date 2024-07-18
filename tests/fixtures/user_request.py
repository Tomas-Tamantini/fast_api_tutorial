import pytest
from fast_api_tutorial.api.dto import CreateUserRequest
from fast_api_tutorial.persistence.models import CreateUserDbRequest


@pytest.fixture
def valid_user_request():
    return {"username": "test", "email": "valid@valid.com", "password": "123"}


@pytest.fixture
def invalid_user_request():
    return {"username": "test", "email": "invalid email", "password": "123"}


@pytest.fixture
def user_request():
    def _create_user_request(
        username: str = "test", email: str = "a@b.com", password: str = "123"
    ) -> CreateUserRequest:
        return CreateUserRequest(username=username, email=email, password=password)

    return _create_user_request


@pytest.fixture
def user_db_request():
    def _create_user_db_request(
        username: str = "test", email: str = "a@b.com", password: str = "123"
    ) -> CreateUserDbRequest:
        return CreateUserDbRequest(username=username, email=email, password=password)

    return _create_user_db_request
