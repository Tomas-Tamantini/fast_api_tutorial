from typing import Annotated
from http import HTTPStatus
from fastapi import Depends, HTTPException
from fast_api_tutorial.api.dependencies.get_unit_of_work import T_UnitOfWork
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


def get_delete_todo_authorization(
    todo_id: int,
    uow: T_UnitOfWork,
) -> DeleteAccountAuthorization:
    with uow:
        todo = uow.todo_repository.get_by_id(todo_id)
        if todo is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        return DeleteAccountAuthorization(target_id=todo.user_id)


T_DeleteTodoAuthorization = Annotated[
    Authorization, Depends(get_delete_todo_authorization)
]
