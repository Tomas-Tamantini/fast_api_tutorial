from abc import ABC, abstractmethod
from fast_api_tutorial.persistence.user_repository import UserRepository
from fast_api_tutorial.persistence.todo_repository import TodoRepository


class UnitOfWork(ABC):
    @property
    @abstractmethod
    def user_repository(self) -> UserRepository:
        pass

    @property
    @abstractmethod
    def todo_repository(self) -> TodoRepository:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.rollback()
