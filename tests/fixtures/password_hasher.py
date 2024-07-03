import pytest
from unittest.mock import MagicMock
from fast_api_tutorial.security import PasswordHasher


@pytest.fixture
def password_hasher():
    hasher = MagicMock(spec=PasswordHasher)
    hasher.hash_password.return_value = "hashed_password"
    hasher.verify_password.return_value = True
    return hasher
