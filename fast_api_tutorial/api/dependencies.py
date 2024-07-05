from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fast_api_tutorial.schemas import (
    User,
)
from fast_api_tutorial.persistence.unit_of_work import UnitOfWork
from fast_api_tutorial.persistence.relational import RelationalUnitOfWork
from fast_api_tutorial.exceptions import (
    NotFoundError,
    BadTokenError,
    CredentialsError,
)
from fast_api_tutorial.settings import Settings
from fast_api_tutorial.security import (
    PasswordHasher,
    PwdLibHasher,
    JwtBuilderProtocol,
    JwtBuilder,
)


def get_unit_of_work() -> UnitOfWork:
    db_url = Settings().DATABASE_URL
    engine = create_engine(db_url)
    session_factory = sessionmaker(bind=engine)
    return RelationalUnitOfWork(session_factory)


def get_password_hasher() -> PasswordHasher:
    return PwdLibHasher()


def get_jwt_builder() -> JwtBuilderProtocol:
    return JwtBuilder(
        secret=Settings().JWT_SECRET,
        expiration_minutes=Settings().JWT_EXPIRATION_MINUTES,
    )


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
