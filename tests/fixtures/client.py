import pytest
from fastapi.testclient import TestClient
from fast_api_tutorial.app import (
    app,
)
from fast_api_tutorial.api import (
    get_unit_of_work,
    get_password_hasher,
    get_jwt_builder,
)


@pytest.fixture
def client(unit_of_work, password_hasher, jwt_builder):
    with TestClient(app) as client:
        app.dependency_overrides[get_unit_of_work] = lambda: unit_of_work
        app.dependency_overrides[get_password_hasher] = lambda: password_hasher
        app.dependency_overrides[get_jwt_builder] = lambda: jwt_builder
        yield client
        app.dependency_overrides.clear()
