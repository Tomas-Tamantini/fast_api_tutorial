import pytest
from unittest.mock import MagicMock
from fast_api_tutorial.persistence.user_repository import UserRepository


@pytest.fixture
def user_repository(user_response):
    repository = MagicMock(spec=UserRepository)
    repository.create.return_value = user_response()
    repository.get_all.return_value = list()
    repository.get.return_value = user_response()
    repository.update.return_value = user_response()
    repository.delete.return_value = None
    return repository
