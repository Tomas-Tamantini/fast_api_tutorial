from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fast_api_tutorial.schemas import CreateUserRequest, UserResponse, UserListResponse
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.persistence.relational import RelationalUnitOfWork
from fast_api_tutorial.exceptions import NotFoundException, DuplicateException
from fast_api_tutorial.settings import Settings
from fast_api_tutorial.security import get_password_hash


app = FastAPI()


def get_unit_of_work() -> UnitOfWork:
    db_url = Settings().DATABASE_URL
    engine = create_engine(db_url)
    session_factory = sessionmaker(bind=engine)
    return RelationalUnitOfWork(session_factory)


def _hashed_password_user(user: CreateUserRequest) -> CreateUserRequest:
    return CreateUserRequest(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/html", response_class=HTMLResponse)
def get_html():
    return """
    <html>
        <head>
            <title>hello world</title>
        </head>
        <body>
            <h1>Hello world!</h1>
            <p>In HTML format :)</p>
        </body>
    </html>
    """


class _UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="User not found")


class _FieldAlreadyInUseError(HTTPException):
    def __init__(self, field: str):
        super().__init__(
            status_code=HTTPStatus.CONFLICT, detail=f"{field} already in use"
        )


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: CreateUserRequest, uow: UnitOfWork = Depends(get_unit_of_work)):
    user = _hashed_password_user(user)
    with uow:
        try:
            uow.user_repository.add(user)
            uow.commit()
            return uow.user_repository.get_from_email(user.email)
        except DuplicateException as e:
            raise _FieldAlreadyInUseError(e.field)


@app.get("/users/", response_model=UserListResponse)
def get_users(
    page: int = 1, size: int = 5, uow: UnitOfWork = Depends(get_unit_of_work)
):
    with uow:
        return {"users": uow.user_repository.get_paginated(page=page, size=size)}


@app.get("/users/{user_id}/", response_model=UserResponse)
def get_user(user_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    with uow:
        try:
            return uow.user_repository.get(user_id)
        except NotFoundException:
            raise _UserNotFoundError()


@app.put("/users/{user_id}/", response_model=UserResponse)
def update_user(
    user_id: int, user: CreateUserRequest, uow: UnitOfWork = Depends(get_unit_of_work)
):
    user = _hashed_password_user(user)
    with uow:
        try:
            uow.user_repository.update(user_id, user)
            uow.commit()
            return uow.user_repository.get(user_id)
        except NotFoundException:
            raise _UserNotFoundError()
        except DuplicateException as e:
            raise _FieldAlreadyInUseError(e.field)


@app.delete("/users/{user_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    with uow:
        try:
            uow.user_repository.delete(user_id)
        except NotFoundException:
            raise _UserNotFoundError()
