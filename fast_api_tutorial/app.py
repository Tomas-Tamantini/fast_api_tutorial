from http import HTTPStatus
from fastapi import FastAPI
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
