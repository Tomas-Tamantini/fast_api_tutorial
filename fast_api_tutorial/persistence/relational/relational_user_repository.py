from sqlalchemy.orm import Session
from fast_api_tutorial.schemas import CreateUserRequest, UserDB
from fast_api_tutorial.persistence.relational.user_model import User


class RelationalUserRepository:
    def __init__(self, session: Session):
        self.session = session

    def add(self, entity: CreateUserRequest) -> UserDB:
        user = User(**entity.model_dump())
        self.session.add(user)
