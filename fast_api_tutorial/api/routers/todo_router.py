from http import HTTPStatus
from fastapi import APIRouter
from fast_api_tutorial.schemas import TodoRequest, TodoResponse
from fast_api_tutorial.api.dependencies import T_UnitOfWork, T_CurrentUser

todo_router = APIRouter(prefix="/todos", tags=["todos"])


@todo_router.post("/", status_code=HTTPStatus.CREATED, response_model=TodoResponse)
def create_todo(
    todo: TodoRequest,
    current_user: T_CurrentUser,
    uow: T_UnitOfWork,
):
    raise NotImplementedError()
