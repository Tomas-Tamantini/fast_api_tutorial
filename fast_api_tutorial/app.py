from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from fast_api_tutorial.schemas import Token
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.exceptions import NotFoundError, WrongUsernameOrPasswordError
from fast_api_tutorial.security import PasswordHasher, JwtBuilderProtocol
from fast_api_tutorial.api.dependencies import (
    get_unit_of_work,
    get_jwt_builder,
    get_password_hasher,
)
from fast_api_tutorial.api.routers import user_router

app = FastAPI()
app.include_router(user_router)


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


@app.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    uow: UnitOfWork = Depends(get_unit_of_work),
    password_hasher: PasswordHasher = Depends(get_password_hasher),
    jwt_builder: JwtBuilderProtocol = Depends(get_jwt_builder),
):
    with uow:
        try:
            user = uow.user_repository.get_from_email(form_data.username)
        except NotFoundError:
            raise WrongUsernameOrPasswordError()
    if not password_hasher.verify_password(form_data.password, user.password):
        raise WrongUsernameOrPasswordError()
    else:
        return jwt_builder.create_token(user.email)
