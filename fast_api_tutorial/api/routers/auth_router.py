from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fast_api_tutorial.api.dto import Token
from fast_api_tutorial.exceptions import NotFoundError, WrongUsernameOrPasswordError
from fast_api_tutorial.api.dependencies import (
    T_UnitOfWork,
    T_JwtBuilder,
    T_PasswordHasher,
    T_CurrentUser,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=Token)
def login(
    password_hasher: T_PasswordHasher,
    jwt_builder: T_JwtBuilder,
    uow: T_UnitOfWork,
    form_data: OAuth2PasswordRequestForm = Depends(),
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


@auth_router.post("/refresh-token", response_model=Token)
def refresh_token(user: T_CurrentUser, jwt_builder: T_JwtBuilder):
    return jwt_builder.create_token(user.email)
