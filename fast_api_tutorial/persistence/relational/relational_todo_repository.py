from sqlalchemy.orm import Session
from fast_api_tutorial.schemas import TodoDbRequest, TodoResponse
from fast_api_tutorial.persistence.relational.todo_model import TodoDB


class RelationalTodoRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: TodoDbRequest) -> TodoResponse:
        todo = TodoDB(**entity.model_dump())
        self._session.add(todo)
