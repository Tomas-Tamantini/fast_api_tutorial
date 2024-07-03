from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fast_api_tutorial.schemas import CreateUserRequest, UserResponse, UserListResponse
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.persistence.relational import RelationalUnitOfWork
from fast_api_tutorial.exceptions import NotFoundException, DuplicateException
from fast_api_tutorial.settings import Settings
from fast_api_tutorial.security import PasswordHasher, PwdLibHasher


app = FastAPI()


def get_unit_of_work() -> UnitOfWork:
    db_url = Settings().DATABASE_URL
    engine = create_engine(db_url)
    session_factory = sessionmaker(bind=engine)
    return RelationalUnitOfWork(session_factory)


def get_password_hasher() -> PasswordHasher:
    return PwdLibHasher()


def _hashed_password_user(
    user: CreateUserRequest, password_hasher: PasswordHasher
) -> CreateUserRequest:
    # TODO: Make this a method of CreateUserRequest
    return CreateUserRequest(
        username=user.username,
        email=user.email,
        password=password_hasher.hash_password(user.password),
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


class _InvalidLoginError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=HTTPStatus.BAD_REQUEST, detail="Wrong email or password"
        )


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(
    user: CreateUserRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
):
    user = _hashed_password_user(user, password_hasher)
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
    user_id: int,
    user: CreateUserRequest,
    uow: UnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
):
    user = _hashed_password_user(user, password_hasher)
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


@app.post("/token")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uow: UnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
):
    with uow:
        try:
            user = uow.user_repository.get_from_email(form_data.username)
        except NotFoundException:
            raise _InvalidLoginError()
    if not password_hasher.verify_password(form_data.password, user.password):
        raise _InvalidLoginError()
    else:
        raise NotImplementedError("Not implemented")
