import pytest
from fast_api_tutorial.core import TodoStatus
from fast_api_tutorial.persistence.models import TodoDbResponse
from datetime import datetime


@pytest.fixture
def todo_response():
    def _todo_response(
        id: int = 1,
        user_id: int = 1,
        title: str = "test",
        description: str = "test",
        status: TodoStatus = TodoStatus.pending,
        created_at: datetime = datetime.now(),
        updated_at: datetime = datetime.now(),
    ) -> TodoDbResponse:
        return TodoDbResponse(
            id=id,
            user_id=user_id,
            title=title,
            description=description,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
        )

    return _todo_response
