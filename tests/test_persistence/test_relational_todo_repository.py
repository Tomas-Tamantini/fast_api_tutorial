import pytest
from sqlalchemy import select
from fast_api_tutorial.persistence.relational import (
    RelationalTodoRepository,
    TodoDB,
    RelationalUserRepository,
)
from fast_api_tutorial.persistence.models import (
    TodoDbRequest,
    PaginationParameters,
    TodoDbFilter,
    CreateUserDbRequest,
)
from fast_api_tutorial.exceptions import NotFoundError


def _add_users(session, num_users: int = 1):
    user_repo = RelationalUserRepository(session)
    for i in range(num_users):
        user = CreateUserDbRequest(
            username=f"name{i}", email=f"email{i}@mail.com", password="123"
        )
        user_repo.add(user)
    session.commit()


@pytest.mark.integration
def test_create_todo_saves_it_to_db(session):
    _add_users(session)
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
    _add_users(session)
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
    _add_users(session)
    repository = RelationalTodoRepository(session)
    repository.add(
        TodoDbRequest(title="test", description="test", status="pending", user_id=1)
    )
    session.commit()
    repository.delete(1)
    assert repository.get_by_id(1) is None


@pytest.mark.integration
def test_getting_todos_returns_paginated_and_filtered_list(session, user_db_request):
    _add_users(session, num_users=2)
    session.commit()
    repository = RelationalTodoRepository(session)
    data = [
        ("laundry", "pending", 1),
        ("dishes", "done", 1),
        ("clean room", "pending", 1),
        ("wash car", "done", 1),
        ("vacuum", "pending", 1),
        ("lawn", "trash", 1),
        ("study", "done", 2),
    ]
    for title, status, user_id in data:
        repository.add(
            TodoDbRequest(
                title=title, description=title, status=status, user_id=user_id
            )
        )
    session.commit()

    pagination = PaginationParameters(limit=2, offset=1)
    filters = TodoDbFilter(user_id=1, status="pending", title=None, description=None)
    todos = repository.get_paginated(pagination, filters)
    titles = [todo.title for todo in todos]
    assert titles == ["clean room", "vacuum"]

    pagination = PaginationParameters(limit=3, offset=2)
    filters = TodoDbFilter(user_id=1, status=None, title="a", description=None)
    todos = repository.get_paginated(pagination, filters)
    titles = [todo.title for todo in todos]
    assert titles == ["wash car", "vacuum", "lawn"]

    pagination = PaginationParameters(limit=3, offset=0)
    filters = TodoDbFilter(user_id=2, status=None, title=None, description=None)
    todos = repository.get_paginated(pagination, filters)
    titles = [todo.title for todo in todos]
    assert titles == ["study"]
