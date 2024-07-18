from typing import Protocol
from fast_api_tutorial.persistence.models import TodoDbRequest, TodoDbResponse


class TodoRepository(Protocol):
    def add(self, entity: TodoDbRequest) -> TodoDbResponse: ...
