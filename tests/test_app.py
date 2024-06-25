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
    response = client.post("/users/", json=request).json()
    assert "password" not in response
    assert response["username"] == request["username"]
    assert response["email"] == request["email"]


def test_get_users_returns_ok(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK


def test_get_users_returns_all_users(client):
    client.post(
        "/users/", json=_create_user_request(is_valid=True)
    )  # TODO: Remove this line by injecting mock DB
    response = client.get("/users/")
    assert "users" in response.json()
    users = response.json()["users"]
    assert len(users) > 0
    assert all("id" in user for user in users)
    assert all("username" in user for user in users)
    assert all("email" in user for user in users)
    assert all("password" not in user for user in users)
