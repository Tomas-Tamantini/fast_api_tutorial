from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fast_api_tutorial.schemas import Token
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.exceptions import NotFoundError, WrongUsernameOrPasswordError
from fast_api_tutorial.security import PasswordHasher, JwtBuilderProtocol
from fast_api_tutorial.api.dependencies import (
    get_unit_of_work,
    get_jwt_builder,
    get_password_hasher,
)

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/token", response_model=Token)
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
