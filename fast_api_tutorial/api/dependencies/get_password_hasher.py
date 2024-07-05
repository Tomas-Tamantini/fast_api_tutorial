from typing import Annotated
from fastapi import Depends
from fast_api_tutorial.security import (
    PasswordHasher,
    PwdLibHasher,
)


def get_password_hasher() -> PasswordHasher:
    return PwdLibHasher()


T_PasswordHasher = Annotated[PasswordHasher, Depends(get_password_hasher)]
