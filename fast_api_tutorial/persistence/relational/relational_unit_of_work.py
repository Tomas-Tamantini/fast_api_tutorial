from typing import Callable
from sqlalchemy.orm.session import Session
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.persistence.relational.relational_user_repository import (
    RelationalUserRepository,
)


class RelationalUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        super().__init__()
        self._session_factory = session_factory
        self._user_repository = None
        self._session = None

    @property
    def user_repository(self) -> RelationalUserRepository:
        if self._user_repository is None:
            self._user_repository = RelationalUserRepository(self._session_factory())
        return self._user_repository

    def __enter__(self):
        self._session = self._session_factory()
        self._user_repository = RelationalUserRepository(self._session)
        return super().__enter__()

    def __exit__(self, *_):
        super().__exit__(*_)
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
