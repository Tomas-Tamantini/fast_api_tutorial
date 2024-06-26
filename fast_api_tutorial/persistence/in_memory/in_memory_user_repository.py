from fast_api_tutorial.schemas import CreateUserRequest, UserDB
from fast_api_tutorial.exceptions import NotFoundException


class InMemoryUserRepository:
    def __init__(self):
        self._users = []

    def _id_to_index(self, id: int) -> int:
        index = id - 1
        if index < 0 or index >= len(self._users):
            raise NotFoundException()
        return index

    @property
    def _next_id(self) -> int:
        return len(self._users) + 1

    def create(self, entity: CreateUserRequest) -> UserDB:
        user_with_id = UserDB(id=self._next_id, **entity.model_dump())
        self._users.append(user_with_id)
        return user_with_id

    def get_all(self) -> list[UserDB]:
        return self._users

    def get(self, id: int) -> UserDB:
        user_index = self._id_to_index(id)
        return self._users[user_index]

    def update(self, id: int, entity: CreateUserRequest) -> UserDB:
        user_index = self._id_to_index(id)
        self._users[user_index] = UserDB(id=id, **entity.model_dump())
        return self._users[user_index]

    def delete(self, id: int) -> None:
        user_index = self._id_to_index(id)
        del self._users[user_index]
