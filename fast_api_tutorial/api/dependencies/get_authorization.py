from typing import Annotated
from fastapi import Depends
from fast_api_tutorial.security import AuthorizationProtocol, Authorization


def get_authorization() -> AuthorizationProtocol:
    return Authorization()


T_Authorization = Annotated[AuthorizationProtocol, Depends(get_authorization)]
