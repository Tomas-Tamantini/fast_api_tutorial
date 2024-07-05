from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fast_api_tutorial.schemas import (
    User,
)
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.exceptions import (
    NotFoundError,
    BadTokenError,
    CredentialsError,
)
from fast_api_tutorial.security import JwtBuilderProtocol
from fast_api_tutorial.api.dependencies.get_unit_of_work import get_unit_of_work
from fast_api_tutorial.api.dependencies.get_jwt_builder import get_jwt_builder

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    uow: UnitOfWork = Depends(get_unit_of_work),
    jwt_builder: JwtBuilderProtocol = Depends(get_jwt_builder),
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
