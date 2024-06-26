from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fast_api_tutorial.schemas import CreateUserRequest, UserResponse, UserListResponse
from fast_api_tutorial.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
from fast_api_tutorial.exceptions import NotFoundException

app = FastAPI()


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


user_repository = InMemoryUserRepository()


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: CreateUserRequest):
    return user_repository.create(user)


@app.get("/users/", response_model=UserListResponse)
def get_users():
    return {"users": user_repository.get_all()}


class _UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="User not found")


@app.get("/users/{user_id}/", response_model=UserResponse)
def get_user(user_id: int):
    try:
        return user_repository.get(user_id)
    except NotFoundException:
        raise _UserNotFoundError()


@app.put("/users/{user_id}/", response_model=UserResponse)
def update_user(user_id: int, user: CreateUserRequest):
    try:
        return user_repository.update(user_id, user)
    except NotFoundException:
        raise _UserNotFoundError()


@app.delete("/users/{user_id}/", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    try:
        user_repository.delete(user_id)
    except NotFoundException:
        raise _UserNotFoundError()
