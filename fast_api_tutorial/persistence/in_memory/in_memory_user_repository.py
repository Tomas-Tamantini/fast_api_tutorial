from fast_api_tutorial.core import User
from fast_api_tutorial.exceptions import NotFoundError, DuplicateFieldError
from fast_api_tutorial.persistence.models import (
    CreateUserDbRequest,
    PaginationParameters,
)


class InMemoryUserRepository:
    def __init__(self):
        self._users = []

    def _id_to_index(self, id: int) -> int:
        index = id - 1
        if index < 0 or index >= len(self._users):
            raise NotFoundError()
        return index

    def add(self, entity: CreateUserDbRequest) -> User:
        for user in self._users:
            if user.email == entity.email:
                raise DuplicateFieldError(field="Email")
            elif user.username == entity.username:
                raise DuplicateFieldError(field="Username")
        self._users.append(User(id=self._next_id, **entity.model_dump()))

    def get_from_email(self, email: str) -> User:
        for user in self._users:
            if user.email == email:
                return user
        raise NotFoundError()

    @property
    def _next_id(self) -> int:
        return len(self._users) + 1

    def get_all(self) -> list[User]:
        return self._users

    def get_paginated(self, pagination: PaginationParameters) -> list[User]:
        start = pagination.offset
        if start >= len(self._users):
            return []
        end = min(start + pagination.limit, len(self._users))
        return self._users[start:end]

    def get(self, id: int) -> User:
        user_index = self._id_to_index(id)
        return self._users[user_index]

    def update(self, id: int, entity: CreateUserDbRequest):
        user_index = self._id_to_index(id)
        self._users[user_index] = User(id=id, **entity.model_dump())

    def delete(self, id: int) -> None:
        user_index = self._id_to_index(id)
        del self._users[user_index]
