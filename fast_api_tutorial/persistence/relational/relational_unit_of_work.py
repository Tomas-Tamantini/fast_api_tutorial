from typing import Callable
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from fast_api_tutorial.exceptions import DuplicateFieldError
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.persistence.relational.relational_user_repository import (
    RelationalUserRepository,
)
from fast_api_tutorial.persistence.relational.relational_todo_repository import (
    RelationalTodoRepository,
)


class RelationalUnitOfWork(UnitOfWork):
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        super().__init__()
        self._session_factory = session_factory
        self._user_repository = None
        self._todo_repository = None
        self._session = None

    @property
    def user_repository(self) -> RelationalUserRepository:
        if self._user_repository is None:
            self._user_repository = RelationalUserRepository(self._session_factory())
        return self._user_repository

    @property
    def todo_repository(self) -> RelationalTodoRepository:
        if self._todo_repository is None:
            self._todo_repository = RelationalTodoRepository(self._session_factory())
        return self._todo_repository

    def __enter__(self):
        self._session = self._session_factory()
        self._user_repository = RelationalUserRepository(self._session)
        self._todo_repository = RelationalTodoRepository(self._session)
        return super().__enter__()

    def __exit__(self, *_):
        super().__exit__(*_)
        self._session.close()

    def commit(self) -> None:
        try:
            self._session.commit()
        except IntegrityError as e:
            self.rollback()
            field = str(e.orig).split(".")[-1].strip()
            raise DuplicateFieldError(field)

    def rollback(self) -> None:
        self._session.rollback()
