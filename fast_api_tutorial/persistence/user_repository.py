from typing import Protocol
from fast_api_tutorial.core import User
from fast_api_tutorial.persistence.models import (
    CreateUserDbRequest,
    PaginationParameters,
)


class UserRepository(Protocol):
    # TODO: Change signature to match todo_repositoty -> get_by_id instead of get, and return None instead of raising NotFoundError

    def add(self, entity: CreateUserDbRequest) -> User: ...

    def get_from_email(self, email: str) -> User: ...

    def get_all(self) -> list[User]: ...

    def get_paginated(self, pagination: PaginationParameters) -> list[User]: ...

    def get(self, id: int) -> User: ...

    def update(self, id: int, entity: CreateUserDbRequest) -> None: ...

    def delete(self, id: int) -> None: ...
