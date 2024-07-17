from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from fast_api_tutorial.persistence.relational.table_registry import table_registry
from fast_api_tutorial.schemas import TodoStatus


@table_registry.mapped_as_dataclass
class TodoDB:
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[TodoStatus]
    user_id: Mapped[int]
