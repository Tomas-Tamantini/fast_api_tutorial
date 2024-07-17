from pydantic import BaseModel
from enum import Enum


class TodoStatus(str, Enum):
    pending = "pending"
    done = "done"


class TodoRequest(BaseModel):
    title: str
    description: str
    status: TodoStatus


class TodoDbRequest(TodoRequest):
    user_id: int

    @classmethod
    def from_todo_request(cls, todo_request: TodoRequest, user_id: int):
        return cls(
            title=todo_request.title,
            description=todo_request.description,
            status=todo_request.status,
            user_id=user_id,
        )


class TodoResponse(TodoRequest):
    id: int
