from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.persistence.in_memory.in_memory_user_repository import (
    InMemoryUserRepository,
)


class InMemoryUnitOfWork(UnitOfWork):
    def __init__(self, users: InMemoryUserRepository):
        self._users = users

    @property
    def user_repository(self) -> InMemoryUserRepository:
        return self._users

    def commit(self) -> None:
        pass

    def rollback(self) -> None:
        pass
