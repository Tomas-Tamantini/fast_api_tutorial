from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_api_tutorial.core import User
from fast_api_tutorial.persistence.relational.user_model import UserDB
from fast_api_tutorial.exceptions import NotFoundError
from fast_api_tutorial.persistence.models import (
    CreateUserDbRequest,
    PaginationParameters,
)


class RelationalUserRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: CreateUserDbRequest) -> User:
        user = UserDB(**entity.model_dump())
        self._session.add(user)
        # TODO: Return the user object with the id

    def get_from_email(self, email: str) -> User:
        result = self._session.scalar(select(UserDB).where(UserDB.email == email))
        if result is None:
            raise NotFoundError()
        else:
            return User.model_validate(result)

    def get_all(self) -> list[User]:
        users = self._session.scalars(select(UserDB))
        return [User.model_validate(user) for user in users]

    def get_paginated(self, pagination: PaginationParameters) -> list[User]:
        users = self._session.scalars(
            select(UserDB).limit(pagination.limit).offset(pagination.offset)
        )
        return [User.model_validate(user) for user in users]

    def get(self, id: int) -> User:
        result = self._session.scalar(select(UserDB).where(UserDB.id == id))
        if result is None:
            raise NotFoundError()
        else:
            return User.model_validate(result)

    def update(self, id: int, entity: CreateUserDbRequest) -> None:
        updated_count = (
            self._session.query(UserDB)
            .filter(UserDB.id == id)
            .update(entity.model_dump())
        )
        if updated_count == 0:
            raise NotFoundError()

    def delete(self, id: int) -> None:
        deleted_count = self._session.query(UserDB).filter(UserDB.id == id).delete()
        if deleted_count == 0:
            raise NotFoundError()
