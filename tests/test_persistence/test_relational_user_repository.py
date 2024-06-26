import pytest
from sqlalchemy import select
from fast_api_tutorial.persistence.relational import RelationalUserRepository, User
from fast_api_tutorial.schemas import CreateUserRequest


@pytest.mark.integration
def test_create_user_saves_it_to_db(session):
    repository = RelationalUserRepository(session)
    repository.add(CreateUserRequest(username="test", email="a@b.com", password="123"))
    session.commit()
    user = session.scalar(select(User).where(User.username == "test"))
    assert user.username == "test"
    assert user.email == "a@b.com"
