from typing import Callable
from pydantic import BaseModel
from fast_api_tutorial.core import UserPublicData, UserCore
from fast_api_tutorial.persistence.models import CreateUserDbRequest


class UserResponse(UserPublicData):
    id: int


class UserListResponse(BaseModel):
    users: list[UserResponse]


class CreateUserRequest(UserCore):
    def with_hashed_password(
        self, hash_method: Callable[[str], str]
    ) -> CreateUserDbRequest:
        return CreateUserDbRequest(
            username=self.username,
            email=self.email,
            password=hash_method(self.password),
        )
