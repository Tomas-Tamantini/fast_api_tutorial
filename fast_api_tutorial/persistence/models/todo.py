from dataclasses import dataclass
from typing import Optional
from fast_api_tutorial.core import TodoCore, Todo, TodoStatus


class TodoDbRequest(TodoCore):
    user_id: int


class TodoDbResponse(Todo):
    user_id: int


@dataclass(frozen=True)
class TodoDbFilter:
    user_id: int
    title: Optional[str]
    description: Optional[str]
    status: Optional[TodoStatus]
