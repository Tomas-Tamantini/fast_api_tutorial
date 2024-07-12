from typing import Protocol
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode, decode, DecodeError
from fast_api_tutorial.schemas import Token
from fast_api_tutorial.exceptions import BadTokenError


class JwtBuilderProtocol(Protocol):
    def create_token(self, bearer: str) -> Token: ...

    def get_token_subject(self, token: str) -> str: ...

    def token_is_expired(self, token: str) -> bool: ...


class JwtBuilder:
    def __init__(self, secret: str, expiration_minutes: int):
        self._secret = secret
        self._algorithm = "HS256"
        self._expiration_minutes = expiration_minutes

    @property
    def algorithm(self) -> str:
        return self._algorithm

    def _expiration(self) -> datetime:
        return datetime.now(ZoneInfo("UTC")) + timedelta(
            minutes=self._expiration_minutes
        )

    def create_token(self, bearer: str) -> Token:
        payload = {"sub": bearer, "exp": self._expiration()}
        access_token = encode(payload, self._secret, algorithm=self._algorithm)
        return Token(access_token=access_token, token_type="bearer")

    def get_token_subject(self, token: str) -> str:
        try:
            return decode(token, self._secret, algorithms=[self._algorithm])["sub"]
        except DecodeError:
            raise BadTokenError()

    def token_is_expired(self, token: str) -> bool:
        return False  # TODO: Implement this method
