from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fast_api_tutorial.schemas import (
    User,
)
from fast_api_tutorial.exceptions import (
    NotFoundError,
    BadTokenError,
    CredentialsError,
)
from fast_api_tutorial.api.dependencies.get_unit_of_work import T_UnitOfWork
from fast_api_tutorial.api.dependencies.get_jwt_builder import T_JwtBuilder

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    jwt_builder: T_JwtBuilder,
    uow: T_UnitOfWork,
    token: str = Depends(oauth2_scheme),
) -> User:
    try:
        email = jwt_builder.get_token_subject(token)
    except BadTokenError:
        raise CredentialsError()
    try:
        return uow.user_repository.get_from_email(email)
    except NotFoundError:
        raise CredentialsError()


T_CurrentUser = Annotated[User, Depends(get_current_user)]
