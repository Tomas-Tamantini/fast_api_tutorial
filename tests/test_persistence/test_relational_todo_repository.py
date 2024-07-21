import pytest
from sqlalchemy import select
from fast_api_tutorial.persistence.relational import RelationalTodoRepository, TodoDB
from fast_api_tutorial.persistence.models import TodoDbRequest
from fast_api_tutorial.exceptions import NotFoundError


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


@pytest.mark.integration
def test_getting_todo_not_in_db_returns_none(session):
    repository = RelationalTodoRepository(session)
    assert repository.get_by_id(1) is None


@pytest.mark.integration
def test_getting_todo_from_db_with_valid_id_returns_todo(session):
    repository = RelationalTodoRepository(session)
    repository.add(
        TodoDbRequest(title="test", description="test", status="pending", user_id=1)
    )
    session.commit()
    todo = repository.get_by_id(1)
    assert todo.title == "test"
    assert todo.description == "test"
    assert todo.status == "pending"
    assert todo.user_id == 1
    assert todo.id == 1


@pytest.mark.integration
def test_deleting_todo_not_in_db_raises_not_found_error(session):
    repository = RelationalTodoRepository(session)
    with pytest.raises(NotFoundError):
        repository.delete(1)


@pytest.mark.integration
def test_deleting_todo_in_db_deletes_it(session):
    repository = RelationalTodoRepository(session)
    repository.add(
        TodoDbRequest(title="test", description="test", status="pending", user_id=1)
    )
    session.commit()
    repository.delete(1)
    assert repository.get_by_id(1) is None
