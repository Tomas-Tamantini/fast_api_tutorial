from typing import Protocol
from fast_api_tutorial.schemas import Token


class JwtBuilderProtocol(Protocol):
    def create_token(self, bearer: str) -> Token: ...


class JwtBuilder:
    def create_token(self, bearer: str) -> Token:
        raise NotImplementedError()
