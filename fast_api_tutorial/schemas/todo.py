from pydantic import BaseModel
from enum import Enum


class TodoStatus(str, Enum):
    pending = "pending"
    done = "done"


class TodoRequest(BaseModel):
    title: str
    description: str
    status: TodoStatus


class TodoResponse(TodoRequest):
    id: int
