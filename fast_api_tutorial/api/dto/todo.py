from fast_api_tutorial.core import TodoCore
from fast_api_tutorial.persistence.models import TodoDbRequest


class TodoRequest(TodoCore):
    def to_db_request(self, user_id: int) -> TodoDbRequest:
        return TodoDbRequest(user_id=user_id, **self.model_dump())