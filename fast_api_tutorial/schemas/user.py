from typing import Callable
from pydantic import BaseModel, EmailStr, ConfigDict


class _UserPublicData(BaseModel):
    model_config = ConfigDict(frozen=True, from_attributes=True)

    username: str
    email: EmailStr


class CreateUserRequest(_UserPublicData):
    password: str

    def with_hashed_password(
        self, hash_method: Callable[[str], str]
    ) -> "CreateUserRequest":
        return CreateUserRequest(
            username=self.username,
            email=self.email,
            password=hash_method(self.password),
        )


class UserDB(CreateUserRequest):
    id: int


class UserResponse(_UserPublicData):
    id: int


class UserListResponse(BaseModel):
    users: list[UserResponse]
