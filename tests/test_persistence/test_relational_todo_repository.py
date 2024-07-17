import pytest
from sqlalchemy import select
from fast_api_tutorial.persistence.relational import RelationalTodoRepository, TodoDB
from fast_api_tutorial.schemas import TodoDbRequest


@pytest.mark.integration
def test_create_todo_saves_it_to_db(session):
    repository = RelationalTodoRepository(session)
    repository.add(
        TodoDbRequest(title="test", description="test", status="pending", user_id=1)
    )
    session.commit()
    todo = session.scalar(select(TodoDB).where(TodoDB.title == "test"))
    assert todo.title == "test"
    assert todo.description == "test"
    assert todo.status == "pending"
    assert todo.user_id == 1
    assert todo.id == 1
