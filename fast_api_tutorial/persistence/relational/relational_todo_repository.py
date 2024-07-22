from typing import Optional
from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from fast_api_tutorial.exceptions import NotFoundError
from fast_api_tutorial.persistence.relational.todo_model import TodoDB
from fast_api_tutorial.persistence.models import (
    TodoDbRequest,
    TodoDbResponse,
    TodoDbFilter,
    PaginationParameters,
)


class RelationalTodoRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: TodoDbRequest) -> TodoDbResponse:
        todo = TodoDB(**entity.model_dump())
        self._session.add(todo)
        self._session.commit()
        self._session.refresh(todo)
        return TodoDbResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
            user_id=todo.user_id,
            created_at=todo.created_at,
            updated_at=todo.updated_at,
        )

    def get_by_id(self, entity_id: int) -> Optional[TodoDbResponse]:
        return self._session.scalar(select(TodoDB).where(TodoDB.id == entity_id))

    def delete(self, entity_id: int) -> None:
        deleted_count = (
            self._session.query(TodoDB).filter(TodoDB.id == entity_id).delete()
        )
        if deleted_count == 0:
            raise NotFoundError()

    def get_paginated(
        self, pagination: PaginationParameters, filters: TodoDbFilter
    ) -> list[TodoDbResponse]:
        query = select(TodoDB).where(TodoDB.user_id == filters.user_id)
        if filters.title:
            query = query.where(TodoDB.title.contains(filters.title))
        if filters.description:
            query = query.where(TodoDB.description.contains(filters.description))
        if filters.status:
            query = query.where(TodoDB.status == filters.status)
        return self._session.scalars(
            query.offset(pagination.offset).limit(pagination.limit)
        ).all()
