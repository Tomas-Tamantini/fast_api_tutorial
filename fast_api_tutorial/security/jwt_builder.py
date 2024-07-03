from typing import Protocol
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode
from fast_api_tutorial.schemas import Token


class JwtBuilderProtocol(Protocol):
    def create_token(self, bearer: str) -> Token: ...


class JwtBuilder:
    def __init__(self, secret: str, algorithm: str, expiration_minutes: int):
        self._secret = secret
        self._algorithm = algorithm
        self._expiration_minutes = expiration_minutes

    def _expiration(self) -> datetime:
        return datetime.now(ZoneInfo("UTC")) + timedelta(
            minutes=self._expiration_minutes
        )

    def create_token(self, bearer: str) -> Token:
        payload = {"sub": bearer, "exp": self._expiration()}
        access_token = encode(payload, self._secret, algorithm=self._algorithm)
        return Token(access_token=access_token, token_type="bearer")
