from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fast_api_tutorial.schemas import (
    CreateUserRequest,
    UserDB,
    UserResponse,
    UserListResponse,
)

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


mock_user_db = []


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: CreateUserRequest):
    user_with_id = UserDB(id=len(mock_user_db) + 1, **user.model_dump())
    mock_user_db.append(user_with_id)
    return user_with_id


@app.get("/users/", response_model=UserListResponse)
def get_users():
    return {"users": mock_user_db}


class _UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=HTTPStatus.NOT_FOUND, detail="User not found")


def _user_id_exists(user_id: int):
    return user_id >= 1 and user_id <= len(mock_user_db)


@app.get("/users/{user_id}/", response_model=UserResponse)
def get_user(user_id: int):
    if _user_id_exists(user_id):
        user_index = user_id - 1
        return mock_user_db[user_index]
    else:
        raise _UserNotFoundError()


@app.put("/users/{user_id}/", response_model=UserResponse)
def update_user(user_id: int, user: CreateUserRequest):
    if _user_id_exists(user_id):
        user_index = user_id - 1
        mock_user_db[user_index] = UserDB(id=user_id, **user.model_dump())
        return mock_user_db[user_index]
    else:
        raise _UserNotFoundError()


@app.delete("/users/{user_id}/", response_model=UserResponse)
def delete_user(user_id: int):
    if _user_id_exists(user_id):
        user_index = user_id - 1
        deleted_user = mock_user_db.pop(user_index)
        return deleted_user
    else:
        raise _UserNotFoundError()
