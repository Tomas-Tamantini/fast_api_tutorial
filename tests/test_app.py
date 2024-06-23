from http import HTTPStatus
from fastapi.testclient import TestClient
from fast_api_tutorial.app import app


def test_read_root_returns_ok():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}
