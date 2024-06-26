from http import HTTPStatus
from fast_api_tutorial.exceptions import NotFoundException


def test_read_root_returns_ok(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


def test_get_html_returns_ok(client):
    response = client.get("/html")
    assert response.status_code == HTTPStatus.OK
    assert "Hello world!" in response.text


def test_create_invalid_user_returns_unprocessable_entity(client, user_request):
    response = client.post("/users/", json=user_request(is_valid=False))
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_valid_user_returns_created(client, user_request):
    response = client.post("/users/", json=user_request(is_valid=True))
    assert response.status_code == HTTPStatus.CREATED


def test_create_valid_user_response_does_not_return_password(
    client, user_repository, user_response, user_request
):
    mock_user = user_response(password="123")
    user_repository.create.return_value = mock_user
    request = user_request(is_valid=True)
    response = client.post("/users/", json=request).json()
    assert "password" not in response
    assert response["username"] == mock_user["username"]
    assert response["email"] == mock_user["email"]


def test_get_users_returns_ok(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK


def test_get_users_returns_all_users(client, user_repository, user_response):
    user_repository.get_all.return_value = [
        user_response(id=123),
        user_response(id=321),
    ]
    response = client.get("/users/")
    assert "users" in response.json()
    users = response.json()["users"]
    assert [user["id"] for user in users] == [123, 321]
    assert not any("password" in user for user in users)


def test_get_user_returns_ok(client):
    response = client.get(f"/users/1/")
    assert response.status_code == HTTPStatus.OK


def test_get_user_returns_user(client, user_repository, user_response):
    mock_user = user_response()
    user_repository.get.return_value = mock_user
    response = client.get(f"/users/1/")
    assert response.json()["id"] == mock_user["id"]
    assert response.json()["username"] == mock_user["username"]
    assert response.json()["email"] == mock_user["email"]
    assert "password" not in response.json()


def test_get_non_existing_user_returns_not_found(client, user_repository):
    user_repository.get.side_effect = NotFoundException
    response = client.get(f"/users/123/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_existing_user_returns_ok(client, user_request):
    response = client.put(f"/users/1/", json=user_request(is_valid=True))
    assert response.status_code == HTTPStatus.OK


def test_update_existing_user_returns_updated_user(
    client, user_repository, user_response, user_request
):
    mock_user = user_response()
    user_repository.update.return_value = mock_user
    response = client.put(f"/users/1/", json=user_request(is_valid=True))
    assert response.json()["username"] == mock_user["username"]
    assert response.json()["id"] == mock_user["id"]


def test_invalid_user_update_returns_unprocessable_entity(client, user_request):
    response = client.put(f"/users/1/", json=user_request(is_valid=False))
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_non_existing_user_returns_not_found(
    client, user_repository, user_request
):
    user_repository.update.side_effect = NotFoundException
    response = client.put(f"/users/123/", json=user_request(is_valid=True))
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_existing_user_returns_no_content(client):
    response = client.delete(f"/users/1/")
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_non_existing_user_returns_not_found(client, user_repository):
    user_repository.delete.side_effect = NotFoundException
    response = client.delete(f"/users/123/")
    assert response.status_code == HTTPStatus.NOT_FOUND
