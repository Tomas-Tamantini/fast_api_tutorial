from http import HTTPStatus


def test_read_exercises_root_returns_ok(client):
    response = client.get("exercises/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


def test_get_html_returns_ok(client):
    response = client.get("exercises/html")
    assert response.status_code == HTTPStatus.OK
    assert "Hello world!" in response.text
