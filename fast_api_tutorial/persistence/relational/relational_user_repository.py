from sqlalchemy import select
from sqlalchemy.orm import Session
from fast_api_tutorial.schemas import CreateUserRequest, UserDB
from fast_api_tutorial.persistence.relational.user_model import User
from fast_api_tutorial.exceptions import NotFoundError


class RelationalUserRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: CreateUserRequest) -> UserDB:
        user = User(**entity.model_dump())
        self._session.add(user)

    def get_from_email(self, email: str) -> UserDB:
        result = self._session.scalar(select(User).where(User.email == email))
        if result is None:
            raise NotFoundError()
        else:
            return UserDB.model_validate(result)

    def get_all(self) -> list[UserDB]:
        users = self._session.scalars(select(User))
        return [UserDB.model_validate(user) for user in users]

    def get_paginated(self, page: int, size: int) -> list[UserDB]:
        offset = (page - 1) * size
        users = self._session.scalars(select(User).limit(size).offset(offset))
        return [UserDB.model_validate(user) for user in users]

    def get(self, id: int) -> UserDB:
        result = self._session.scalar(select(User).where(User.id == id))
        if result is None:
            raise NotFoundError()
        else:
            return UserDB.model_validate(result)

    def update(self, id: int, entity: CreateUserRequest) -> None:
        updated_count = (
            self._session.query(User).filter(User.id == id).update(entity.model_dump())
        )
        if updated_count == 0:
            raise NotFoundError()

    def delete(self, id: int) -> None:
        deleted_count = self._session.query(User).filter(User.id == id).delete()
        if deleted_count == 0:
            raise NotFoundError()
