import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from fast_api_tutorial.app import app, get_unit_of_work
from fast_api_tutorial.persistence.user_repository import UserRepository


@pytest.fixture
def user_repository():
    yield MagicMock(spec=UserRepository)


@pytest.fixture
def unit_of_work(user_repository):
    with MagicMock() as mock:
        mock.user_repository = user_repository
        yield mock


@pytest.fixture
def client(unit_of_work):
    with TestClient(app) as client:
        app.dependency_overrides[get_unit_of_work] = lambda: unit_of_work
        yield client
        app.dependency_overrides.clear()
