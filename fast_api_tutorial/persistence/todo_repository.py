from typing import Protocol
from fast_api_tutorial.schemas import TodoDbRequest, TodoResponse


class TodoRepository(Protocol):
    def add(self, entity: TodoDbRequest) -> TodoResponse: ...
