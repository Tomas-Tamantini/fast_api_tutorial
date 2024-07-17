import pytest
from fast_api_tutorial.schemas import TodoResponse, TodoStatus


@pytest.fixture
def todo_response():
    def _todo_response(
        id: int = 1,
        title: str = "test",
        description: str = "test",
        status: TodoStatus = TodoStatus.pending,
    ) -> TodoResponse:
        return TodoResponse(id=id, title=title, description=description, status=status)

    return _todo_response
