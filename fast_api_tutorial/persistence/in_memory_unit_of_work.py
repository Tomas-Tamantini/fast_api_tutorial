from fast_api_tutorial.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork


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
