from sqlalchemy.orm import Session
from fast_api_tutorial.schemas import TodoDbRequest, TodoResponse
from fast_api_tutorial.persistence.relational.todo_model import TodoDB


class RelationalTodoRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: TodoDbRequest) -> TodoResponse:
        todo = TodoDB(**entity.model_dump())
        self._session.add(todo)
        self._session.commit()
        self._session.refresh(todo)
        return TodoResponse(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
        )
