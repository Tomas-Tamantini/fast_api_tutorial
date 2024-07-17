import pytest
from unittest.mock import MagicMock


@pytest.fixture
def unit_of_work(user_repository, todo_repository):
    with MagicMock() as mock:
        mock.user_repository = user_repository
        mock.todo_repository = todo_repository
        yield mock
