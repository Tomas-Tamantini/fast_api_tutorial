from typing import Callable
from pydantic import BaseModel, EmailStr, ConfigDict


class UserPublicData(BaseModel):
    model_config = ConfigDict(frozen=True, from_attributes=True)

    username: str
    email: EmailStr


class UserCore(UserPublicData):
    password: str


class User(UserCore):
    id: int
