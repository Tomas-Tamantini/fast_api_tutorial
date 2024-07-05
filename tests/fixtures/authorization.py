import pytest
from unittest.mock import MagicMock
from fast_api_tutorial.security import Authorization


@pytest.fixture
def authorization():
    auth = MagicMock(spec=Authorization)
    auth.has_permission.return_value = True
    return auth
