from typing import Annotated
from fastapi import Depends
from fast_api_tutorial.security import (
    Authorization,
    DeleteAccountAuthorization,
    UpdateAccountAuthorization,
)


def get_delete_account_authorization(user_id: int) -> DeleteAccountAuthorization:
    return DeleteAccountAuthorization(target_id=user_id)


T_DeleteAccountAuthorization = Annotated[
    Authorization, Depends(get_delete_account_authorization)
]


def get_update_account_authorization(user_id: int) -> UpdateAccountAuthorization:
    return UpdateAccountAuthorization(target_id=user_id)


T_UpdateAccountAuthorization = Annotated[
    Authorization, Depends(get_update_account_authorization)
]
