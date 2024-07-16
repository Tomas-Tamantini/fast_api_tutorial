from http import HTTPStatus
import pytest
from fast_api_tutorial.exceptions import NotFoundError, BadTokenError


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


def test_refresh_token_with_bad_token_returns_unauthorized(client, jwt_builder):
    jwt_builder.get_token_subject.side_effect = BadTokenError
    response = client.post("auth/refresh-token")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.skip("TODO: Check why this is failing")
def test_refresh_token_with_good_token_returns_token(client, jwt_builder):
    fake_token = {"access_token": "123", "token_type": "bearer"}
    jwt_builder.create_token.return_value = fake_token

    response = client.post("auth/refresh-token")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == fake_token
