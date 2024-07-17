import pytest


@pytest.fixture
def valid_todo_request():
    return {
        "title": "test",
        "description": "test",
        "status": "pending",
    }
