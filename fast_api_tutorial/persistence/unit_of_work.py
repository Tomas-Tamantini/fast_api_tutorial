from abc import ABC, abstractmethod
from fast_api_tutorial.persistence.user_repository import UserRepository


class UnitOfWork(ABC):
    @property
    @abstractmethod
    def user_repository(self) -> UserRepository:
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
