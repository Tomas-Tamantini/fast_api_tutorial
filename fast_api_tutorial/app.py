from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse
from fast_api_tutorial.schemas import CreateUserRequest, UserResponse, UserListResponse
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.persistence.in_memory import (
    InMemoryUnitOfWork,
    InMemoryUserRepository,
)
from fast_api_tutorial.exceptions import NotFoundException

app = FastAPI()
users_repository = InMemoryUserRepository()


def get_unit_of_work() -> UnitOfWork:
    return InMemoryUnitOfWork(users_repository)


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


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: CreateUserRequest, uow: UnitOfWork = Depends(get_unit_of_work)):
    with uow:
        uow.user_repository.add(user)
        uow.commit()
        return uow.user_repository.get_from_email(user.email)


@app.get("/users/", response_model=UserListResponse)
def get_users(uow: UnitOfWork = Depends(get_unit_of_work)):
    with uow:
        return {"users": uow.user_repository.get_all()}


class _UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="User not found")


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
    with uow:
        try:
            uow.user_repository.update(user_id, user)
            uow.commit()
            return uow.user_repository.get(user_id)
        except NotFoundException:
            raise _UserNotFoundError()


@app.delete("/users/{user_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int, uow: UnitOfWork = Depends(get_unit_of_work)):
    with uow:
        try:
            uow.user_repository.delete(user_id)
        except NotFoundException:
            raise _UserNotFoundError()
