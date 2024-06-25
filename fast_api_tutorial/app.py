from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fast_api_tutorial.schemas import CreateUserRequest, CreateUserResponse

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


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=CreateUserResponse)
def create_user(user: CreateUserRequest):
    return user
