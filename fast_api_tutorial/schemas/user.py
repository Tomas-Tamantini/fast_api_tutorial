from pydantic import BaseModel, EmailStr


class _UserPublicData(BaseModel):
    username: str
    email: EmailStr


class CreateUserRequest(_UserPublicData):
    password: str


class UserDB(CreateUserRequest):
    id: int


class UserResponse(_UserPublicData):
    id: int
