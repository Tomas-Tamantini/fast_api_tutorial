import pytest
from unittest.mock import MagicMock
from fast_api_tutorial.security import JwtBuilderProtocol
from fast_api_tutorial.schemas import Token


@pytest.fixture
def jwt_builder():
    builder = MagicMock(spec=JwtBuilderProtocol)
    builder.create_token.return_value = Token(
        access_token="access_token", token_type="bearer"
    )
    return builder
