import pytest
from unittest.mock import MagicMock
from fast_api_tutorial.persistence.todo_repository import TodoRepository


@pytest.fixture
def todo_repository(todo_response):
    repository = MagicMock(spec=TodoRepository)
    repository.add.return_value = todo_response()
    repository.get_by_id.return_value = todo_response()
    repository.get_paginated.return_value = []
    return repository
