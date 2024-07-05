from fast_api_tutorial.security import (
    PasswordHasher,
    PwdLibHasher,
)


def get_password_hasher() -> PasswordHasher:
    return PwdLibHasher()
