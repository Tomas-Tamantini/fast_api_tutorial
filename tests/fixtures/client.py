import pytest
from fastapi.testclient import TestClient
from fast_api_tutorial.app import app, get_unit_of_work


@pytest.fixture
def client(unit_of_work):
    with TestClient(app) as client:
        app.dependency_overrides[get_unit_of_work] = lambda: unit_of_work
        yield client
        app.dependency_overrides.clear()
