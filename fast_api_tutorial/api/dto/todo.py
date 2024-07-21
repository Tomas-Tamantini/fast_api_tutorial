from typing import Optional
from pydantic import BaseModel
from fast_api_tutorial.core import TodoCore, Todo, TodoStatus
from fast_api_tutorial.persistence.models import (
    TodoDbRequest,
    PaginationParameters,
    TodoDbFilter,
)


class TodoRequest(TodoCore):
    def to_db_request(self, user_id: int) -> TodoDbRequest:
        return TodoDbRequest(user_id=user_id, **self.model_dump())


class TodoListResponse(BaseModel):
    todos: list[Todo]


class GetTodosQueryParams(BaseModel):
    limit: int = 10
    offset: int = 0
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TodoStatus] = None

    def pagination(self) -> PaginationParameters:
        return PaginationParameters(limit=self.limit, offset=self.offset)

    def filters(self, user_id: int) -> TodoDbFilter:
        return TodoDbFilter(
            user_id=user_id,
            title=self.title,
            description=self.description,
            status=self.status,
        )
