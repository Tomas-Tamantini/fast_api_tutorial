import pytest
from unittest.mock import MagicMock
from fast_api_tutorial.security import AuthorizationProtocol


@pytest.fixture
def authorization():
    auth = MagicMock(spec=AuthorizationProtocol)
    auth.can_delete_account.return_value = True
    auth.can_update_account.return_value = True
    return auth
