from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class TodoStatus(str, Enum):
    pending = "pending"
    done = "done"
    trash = "trash"


class TodoCore(BaseModel):
    title: str
    description: str
    status: TodoStatus


class Todo(TodoCore):
    id: int
    created_at: datetime
    updated_at: datetime
