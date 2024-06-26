from pydantic import BaseModel, EmailStr, ConfigDict


class _UserPublicData(BaseModel):
    model_config = ConfigDict(frozen=True, from_attributes=True)

    username: str
    email: EmailStr


class CreateUserRequest(_UserPublicData):
    password: str


class UserDB(CreateUserRequest):
    id: int


class UserResponse(_UserPublicData):
    id: int


class UserListResponse(BaseModel):
    users: list[UserResponse]
