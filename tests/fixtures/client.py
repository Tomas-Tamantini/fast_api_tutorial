import pytest
from fastapi.testclient import TestClient
from fast_api_tutorial.app import app, get_unit_of_work, get_password_hasher


@pytest.fixture
def client(unit_of_work, password_hasher):
    with TestClient(app) as client:
        app.dependency_overrides[get_unit_of_work] = lambda: unit_of_work
        app.dependency_overrides[get_password_hasher] = lambda: password_hasher
        yield client
        app.dependency_overrides.clear()
