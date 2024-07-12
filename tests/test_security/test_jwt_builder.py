import pytest
from jwt import decode
from fast_api_tutorial.exceptions import BadTokenError
from fast_api_tutorial.security import JwtBuilder
from freezegun import freeze_time


def test_jwt_builder_returns_bearer_token_type():
    token_builder = JwtBuilder(secret="secret", expiration_minutes=10)
    token = token_builder.create_token(bearer="a@b.com")
    assert token.token_type == "bearer"


def _decode_jwt(email: str = "a@b.com", expiration_minutes: int = 10) -> dict:
    secret = "secret"
    token_builder = JwtBuilder(secret, expiration_minutes)
    token = token_builder.create_token(email)
    return decode(token.access_token, secret, algorithms=[token_builder.algorithm])


def test_jwt_builder_puts_email_in_subject():
    email = "a@b.com"
    payload = _decode_jwt(email)
    assert payload["sub"] == email


def test_jwt_builder_includes_expiration():
    expiration_minutes = 10
    with freeze_time("2024-07-12 21:47:17"):
        payload = _decode_jwt(expiration_minutes=expiration_minutes)
        assert payload["exp"] == 1720821437


def test_jwt_builder_extracts_subject_from_token():
    email = "a@b.com"
    secret = "secret"
    token_builder = JwtBuilder(secret, expiration_minutes=10)
    token = token_builder.create_token(email)
    subject = token_builder.get_token_subject(token.access_token)
    assert subject == email


def test_bad_jwt_raises_bad_token_error_on_decode():
    builder = JwtBuilder(secret="secret", expiration_minutes=10)
    bad_token = "bad"
    with pytest.raises(BadTokenError):
        builder.get_token_subject(bad_token)


def test_jwt_builder_checks_if_token_is_expired():
    with freeze_time("2021-01-01 12:00:00"):
        token_builder = JwtBuilder(secret="secret", expiration_minutes=10)
        token = token_builder.create_token("bearer").access_token

    with freeze_time("2021-01-01 12:09:59"):
        token_builder.get_token_subject(token)

    with freeze_time("2021-01-01 12:10:01"):
        with pytest.raises(BadTokenError):
            token_builder.get_token_subject(token)
