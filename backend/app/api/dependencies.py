from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..repositories.todo_repository import TodoRepository
from ..services.todo_service import TodoService


def get_todo_service(db: Annotated[Session, Depends(get_db)]) -> TodoService:
    return TodoService(TodoRepository(db))
