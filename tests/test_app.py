from http import HTTPStatus
from fast_api_tutorial.schemas import User
from fast_api_tutorial.exceptions import (
    NotFoundError,
    DuplicateFieldError,
    BadTokenError,
)


def test_read_exercises_root_returns_ok(client):
    response = client.get("exercises/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Hello World"}


def test_get_html_returns_ok(client):
    response = client.get("exercises/html")
    assert response.status_code == HTTPStatus.OK
    assert "Hello world!" in response.text


def test_create_invalid_user_returns_unprocessable_entity(client, invalid_user_request):
    response = client.post("/users/", json=invalid_user_request)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_create_valid_user_returns_created(client, valid_user_request):
    response = client.post("/users/", json=valid_user_request)
    assert response.status_code == HTTPStatus.CREATED


def test_create_valid_user_hashes_password_before_saving(
    client, user_repository, user_request, password_hasher
):
    request = user_request(password="123")
    password_hasher.hash_password.return_value = "hashed_password"
    client.post("/users/", json=request.dict())
    assert user_repository.add.call_args[0][0].password == "hashed_password"


def test_create_valid_user_response_does_not_return_password(
    client, user_repository, user_response, valid_user_request
):
    mock_user = user_response(password="123")
    user_repository.get_from_email.return_value = mock_user
    request = valid_user_request
    response = client.post("/users/", json=request).json()
    assert "password" not in response
    assert response["username"] == mock_user.username
    assert response["email"] == mock_user.email


def test_create_valid_user_commits_changes(client, unit_of_work, valid_user_request):
    client.post("/users/", json=valid_user_request)
    assert unit_of_work.commit.called


def test_get_users_returns_ok(client):
    response = client.get("/users/")
    assert response.status_code == HTTPStatus.OK


def test_get_users_returns_paginated_users(client, user_repository, user_response):
    user_repository.get_paginated.return_value = [
        user_response(id=123),
        user_response(id=321),
    ]
    response = client.get("/users/", params={"page": 1, "size": 2})
    assert "users" in response.json()
    users = response.json()["users"]
    assert [user["id"] for user in users] == [123, 321]
    assert not any("password" in user for user in users)
    assert user_repository.get_paginated.call_args[1] == {"page": 1, "size": 2}


def test_get_user_returns_ok(client):
    response = client.get("/users/1/")
    assert response.status_code == HTTPStatus.OK


def test_get_user_returns_user(client, user_repository, user_response):
    mock_user = user_response()
    user_repository.get.return_value = mock_user
    response = client.get("/users/1/")
    assert response.json()["id"] == mock_user.id
    assert response.json()["username"] == mock_user.username
    assert response.json()["email"] == mock_user.email
    assert "password" not in response.json()


def test_get_non_existing_user_returns_not_found(client, user_repository):
    user_repository.get.side_effect = NotFoundError
    response = client.get("/users/123/")
    assert response.status_code == HTTPStatus.NOT_FOUND


def _make_put_request(
    client, user_id: int = 1, request: dict = None, token: str = "good_token"
):
    request = request or {
        "username": "test",
        "email": "valid@valid.com",
        "password": "123",
    }
    return client.put(
        f"/users/{user_id}/",
        headers={"Authorization": f"Bearer {token}"},
        json=request,
    )


def test_update_existing_user_returns_ok(client, valid_user_request):
    response = _make_put_request(client, request=valid_user_request)
    assert response.status_code == HTTPStatus.OK


def test_update_existing_user_returns_updated_user(
    client, user_repository, user_response, valid_user_request
):
    mock_user = user_response()
    user_repository.get.return_value = mock_user
    response = _make_put_request(client, request=valid_user_request)
    assert response.json()["username"] == mock_user.username
    assert response.json()["id"] == mock_user.id


def test_updating_existing_user_commits_changes(
    client, unit_of_work, valid_user_request
):
    _make_put_request(client, request=valid_user_request)
    assert unit_of_work.commit.called


def test_update_existing_user_hashes_password_before_saving(
    client, user_repository, user_request, password_hasher
):
    request = user_request(password="123")
    password_hasher.hash_password.return_value = "hashed_password"
    _make_put_request(client, request=request.dict())
    assert user_repository.update.call_args[0][1].password == "hashed_password"


def test_invalid_user_update_returns_unprocessable_entity(client, invalid_user_request):
    response = _make_put_request(client, request=invalid_user_request)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_non_existing_user_returns_not_found(
    client, user_repository, valid_user_request
):
    user_repository.update.side_effect = NotFoundError
    response = _make_put_request(client, request=valid_user_request)
    assert response.status_code == HTTPStatus.NOT_FOUND


def _make_delete_request(client, user_id: int = 1, token: str = "good_token"):
    return client.delete(
        f"/users/{user_id}/", headers={"Authorization": f"Bearer {token}"}
    )


def test_delete_existing_user_returns_no_content(client):
    response = _make_delete_request(client)
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_existing_user_returns_commits_deletion(client, unit_of_work):
    _make_delete_request(client)
    assert unit_of_work.commit.called


def test_delete_non_existing_user_returns_not_found(client, user_repository):
    user_repository.delete.side_effect = NotFoundError
    response = _make_delete_request(client, user_id=1)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_creating_user_with_conflicting_field_returns_conflict(
    client, unit_of_work, valid_user_request
):
    unit_of_work.commit.side_effect = DuplicateFieldError(field="Email")
    response = client.post("/users/", json=valid_user_request)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Email already in use"


def test_updating_user_with_conflicting_field_returns_conflict(
    client, unit_of_work, valid_user_request
):
    unit_of_work.commit.side_effect = DuplicateFieldError(field="Username")
    response = _make_put_request(client, request=valid_user_request)
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()["detail"] == "Username already in use"


def test_login_with_bad_username_returns_bad_request(
    client, user_repository, password_hasher
):
    user_repository.get_from_email.side_effect = NotFoundError
    password_hasher.verify_password.return_value = True
    response = client.post("auth/token", data={"username": "bad", "password": "bad"})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_with_bad_password_returns_bad_request(client, password_hasher):
    password_hasher.verify_password.return_value = False
    response = client.post("auth/token", data={"username": "email", "password": "bad"})
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_successful_login_returns_jwt(
    client, user_repository, user_response, password_hasher, jwt_builder
):
    password_hasher.verify_password.return_value = True
    fake_user = user_response(email="a@b.com")
    user_repository.get_from_email.return_value = fake_user
    fake_token = {"access_token": "123", "token_type": "bearer"}
    jwt_builder.create_token.return_value = fake_token
    response = client.post(
        "auth/token", data={"username": "email", "password": "password"}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == fake_token
    assert jwt_builder.create_token.call_args[0][0] == "a@b.com"


def test_update_user_returns_unauthorized_if_could_not_decode_token(
    client, jwt_builder
):
    jwt_builder.get_token_subject.side_effect = BadTokenError
    response = _make_put_request(client, token="bad_token")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert jwt_builder.get_token_subject.call_args[0][0] == "bad_token"


def test_update_user_returns_unauthorized_if_user_not_in_database(
    client, user_repository
):
    user_repository.get_from_email.side_effect = NotFoundError
    response = _make_put_request(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_user_returns_forbidden_if_user_not_trying_to_update_other_account(
    client, user_repository
):
    bearer_id = 123
    update_id = 321
    user_repository.get_from_email.return_value = User(
        id=bearer_id, username="user", email="a@b.com", password="123"
    )
    response = _make_put_request(client, user_id=update_id)
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_delete_user_returns_unauthorized_if_could_not_decode_token(
    client, jwt_builder
):
    jwt_builder.get_token_subject.side_effect = BadTokenError
    response = _make_delete_request(client, token="bad_token")
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert jwt_builder.get_token_subject.call_args[0][0] == "bad_token"


def test_delete_user_returns_unauthorized_if_user_not_in_database(
    client, user_repository
):
    user_repository.get_from_email.side_effect = NotFoundError
    response = _make_delete_request(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user_returns_forbidden_if_user_not_trying_to_delete_other_account(
    client, user_repository
):
    bearer_id = 123
    delete_id = 321
    user_repository.get_from_email.return_value = User(
        id=bearer_id, username="user", email="a@b.com", password="123"
    )
    response = _make_delete_request(client, user_id=delete_id)
    assert response.status_code == HTTPStatus.FORBIDDEN
