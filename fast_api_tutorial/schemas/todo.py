from pydantic import BaseModel
from enum import Enum


class TodoStatus(str, Enum):
    pending = "pending"
    done = "done"
    trash = "trash"


class TodoCore(BaseModel):
    title: str
    description: str
    status: TodoStatus


class TodoDbRequest(TodoCore):
    user_id: int


class TodoRequest(TodoCore):
    def to_db_request(self, user_id: int):
        return TodoDbRequest(user_id=user_id, **self.model_dump())


class TodoResponse(TodoRequest):
    id: int
