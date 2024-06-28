from fast_api_tutorial.schemas import CreateUserRequest, UserDB
from fast_api_tutorial.exceptions import NotFoundException, DuplicateException


class InMemoryUserRepository:
    def __init__(self):
        self._users = []

    def _id_to_index(self, id: int) -> int:
        index = id - 1
        if index < 0 or index >= len(self._users):
            raise NotFoundException()
        return index

    def add(self, entity: CreateUserRequest) -> None:
        for user in self._users:
            if user.email == entity.email:
                raise DuplicateException(field="Email")
            elif user.username == entity.username:
                raise DuplicateException(field="Username")
        self._users.append(UserDB(id=self._next_id, **entity.model_dump()))

    def get_from_email(self, email: str) -> UserDB:
        for user in self._users:
            if user.email == email:
                return user
        raise NotFoundException()

    @property
    def _next_id(self) -> int:
        return len(self._users) + 1

    def get_all(self) -> list[UserDB]:
        return self._users

    def get_paginated(self, page: int, size: int) -> list[UserDB]:
        start = (page - 1) * size
        end = start + size
        return self._users[start:end]

    def get(self, id: int) -> UserDB:
        user_index = self._id_to_index(id)
        return self._users[user_index]

    def update(self, id: int, entity: CreateUserRequest):
        user_index = self._id_to_index(id)
        self._users[user_index] = UserDB(id=id, **entity.model_dump())

    def delete(self, id: int) -> None:
        user_index = self._id_to_index(id)
        del self._users[user_index]
