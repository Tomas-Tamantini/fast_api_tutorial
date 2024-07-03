from fast_api_tutorial.security import PwdLibHasher, JwtBuilder
from jwt import decode


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
    token_builder = JwtBuilder(
        secret="secret", algorithm="HS256", expiration_minutes=10
    )
    token = token_builder.create_token(bearer="a@b.com")
    assert token.token_type == "bearer"


def _decode_jwt(email: str = "a@b.com", expiration_minutes: int = 10) -> dict:
    secret = "secret"
    algorithm = "HS256"
    token_builder = JwtBuilder(secret, algorithm, expiration_minutes)
    token = token_builder.create_token(email)
    return decode(token.access_token, secret, algorithms=[algorithm])


def test_jwt_builder_puts_email_in_subject():
    email = "a@b.com"
    payload = _decode_jwt(email)
    assert payload["sub"] == email


def test_jwt_builder_includes_expiration():
    expiration_minutes = 10
    payload = _decode_jwt(expiration_minutes=expiration_minutes)
    assert "exp" in payload
    # TODO: Check that the expiration is within 10 minutes
