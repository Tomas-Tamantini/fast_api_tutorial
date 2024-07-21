from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from fast_api_tutorial.api.dto import TodoRequest
from fast_api_tutorial.core import Todo
from fast_api_tutorial.api.dependencies import (
    T_UnitOfWork,
    T_CurrentUser,
    T_DeleteTodoAuthorization,
)
from fast_api_tutorial.exceptions import NotFoundError

todo_router = APIRouter(prefix="/todos", tags=["todos"])


@todo_router.post("/", status_code=HTTPStatus.CREATED, response_model=Todo)
def create_todo(
    todo: TodoRequest,
    current_user: T_CurrentUser,
    uow: T_UnitOfWork,
):
    db_request = todo.to_db_request(current_user.id)
    with uow:
        response = uow.todo_repository.add(db_request)
        uow.commit()
        return response


@todo_router.delete("/{todo_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_todo(
    todo_id: int,
    current_user: T_CurrentUser,
    uow: T_UnitOfWork,
    authorization: T_DeleteTodoAuthorization,
):
    if not authorization.has_permission(current_user.id):
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN)
    with uow:
        try:
            uow.todo_repository.delete(todo_id)
            uow.commit()
        except NotFoundError:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
