import pytest
from jwt import decode
from fast_api_tutorial.exceptions import BadTokenError
from fast_api_tutorial.security import PwdLibHasher, JwtBuilder


def test_pwdlib_hasher_hashes_password():
    password = "123"
    hashed = PwdLibHasher().hash_password(password)
    assert hashed != password


def test_pwdlib_hasher_verifies_password():
    password = "123"
    hasher = PwdLibHasher()
    hashed = hasher.hash_password(password)
    assert hasher.verify_password(password, hashed)
    assert not hasher.verify_password("wrong", hashed)


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
    payload = _decode_jwt(expiration_minutes=expiration_minutes)
    assert "exp" in payload
    # TODO: Check that the expiration is within 10 minutes


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
