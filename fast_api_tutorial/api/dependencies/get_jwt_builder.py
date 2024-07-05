from typing import Annotated
from fastapi import Depends
from fast_api_tutorial.settings import Settings
from fast_api_tutorial.security import JwtBuilderProtocol, JwtBuilder


def get_jwt_builder() -> JwtBuilderProtocol:
    return JwtBuilder(
        secret=Settings().JWT_SECRET,
        expiration_minutes=Settings().JWT_EXPIRATION_MINUTES,
    )


T_JwtBuilder = Annotated[JwtBuilderProtocol, Depends(get_jwt_builder)]
