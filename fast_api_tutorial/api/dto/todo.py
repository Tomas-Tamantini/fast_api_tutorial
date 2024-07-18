from fast_api_tutorial.schemas import TodoCore
from fast_api_tutorial.persistence.models import TodoDbRequest


class TodoRequest(TodoCore):
    def to_db_request(self, user_id: int) -> TodoDbRequest:
        return TodoDbRequest(user_id=user_id, **self.model_dump())


class TodoResponse(TodoCore):
    id: int
