from typing import Protocol, Optional
from fast_api_tutorial.persistence.models import (
    TodoDbRequest,
    TodoDbResponse,
    TodoDbFilter,
    PaginationParameters,
)


class TodoRepository(Protocol):
    def add(self, entity: TodoDbRequest) -> TodoDbResponse: ...

    def get_by_id(self, entity_id: int) -> Optional[TodoDbResponse]: ...

    def delete(self, entity_id: int) -> None: ...

    def get_paginated(
        self, pagination: PaginationParameters, filters: TodoDbFilter
    ) -> list[TodoDbResponse]: ...
