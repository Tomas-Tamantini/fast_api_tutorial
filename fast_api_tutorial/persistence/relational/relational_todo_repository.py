from sqlalchemy.orm import Session
from fast_api_tutorial.core import Todo
from fast_api_tutorial.persistence.models import TodoDbRequest
from fast_api_tutorial.persistence.relational.todo_model import TodoDB


class RelationalTodoRepository:
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: TodoDbRequest) -> Todo:
        todo = TodoDB(**entity.model_dump())
        self._session.add(todo)
        self._session.commit()
        self._session.refresh(todo)
        return Todo(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=todo.status,
        )
