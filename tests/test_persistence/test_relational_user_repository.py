from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from fast_api_tutorial.persistence.relational import (
    table_registry,
    User,
    RelationalUserRepository,
)
from fast_api_tutorial.schemas import CreateUserRequest


def test_create_user_saves_it_to_db():
    engine = create_engine("sqlite:///:memory:")
    table_registry.metadata.create_all(engine)
    with Session(engine) as session:
        repository = RelationalUserRepository(session)
        repository.add(
            CreateUserRequest(username="test", email="a@b.com", password="123")
        )
        session.commit()
        user = session.scalar(select(User).where(User.username == "test"))
        assert user.username == "test"
        assert user.email == "a@b.com"
    table_registry.metadata.drop_all(engine)
