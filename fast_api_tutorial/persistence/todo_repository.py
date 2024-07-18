from typing import Protocol
from fast_api_tutorial.persistence.models import TodoDbRequest
from fast_api_tutorial.core import Todo


class TodoRepository(Protocol):
    def add(self, entity: TodoDbRequest) -> Todo: ...
