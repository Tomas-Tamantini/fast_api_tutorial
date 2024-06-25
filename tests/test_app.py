from http import HTTPStatus


def test_read_root_returns_ok(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


def test_get_html_returns_ok(client):
    response = client.get("/html")
    assert response.status_code == HTTPStatus.OK
    assert "Hello world!" in response.text


def _create_user_request(is_valid: bool) -> dict:
    return {
        "username": "test",
        "email": "valid@valid.com" if is_valid else "invalid email",
        "password": "password",
    }


def test_create_invalid_user_returns_unprocessable_entity(client):
    response = client.post("/users/", json=_create_user_request(is_valid=False))
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_valid_user_returns_created(client):
    response = client.post("/users/", json=_create_user_request(is_valid=True))
    assert response.status_code == HTTPStatus.CREATED


def test_create_valid_user_response_does_not_return_password(client):
    request = _create_user_request(is_valid=True)
    response = client.post("/users/", json=request)
    assert response.json() == {
        "username": request["username"],
        "email": request["email"],
    }
