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
