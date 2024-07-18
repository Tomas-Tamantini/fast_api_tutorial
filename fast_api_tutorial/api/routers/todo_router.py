from http import HTTPStatus
from fastapi import APIRouter
from fast_api_tutorial.api.dto import TodoRequest
from fast_api_tutorial.core import Todo
from fast_api_tutorial.api.dependencies import T_UnitOfWork, T_CurrentUser

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
