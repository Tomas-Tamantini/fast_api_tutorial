from http import HTTPStatus
from fastapi import HTTPException


class NotFoundError(Exception): ...


class DuplicateFieldError(Exception):
    def __init__(self, field: str) -> None:
        self.field = field
        super().__init__(f"Duplicate value for field {field}")


class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="User not found")


class FieldAlreadyInUseError(HTTPException):
    def __init__(self, field: str):
        super().__init__(
            status_code=HTTPStatus.CONFLICT, detail=f"{field} already in use"
        )


class WrongUsernameOrPasswordError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST, detail="Wrong email or password"
        )
