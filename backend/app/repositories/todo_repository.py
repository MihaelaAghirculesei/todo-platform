from datetime import datetime, timezone

from sqlalchemy.orm import Session

from ..models.todo_model import TodoModel
from ..schemas.todo import TodoOut


class TodoRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_all(self) -> list[TodoOut]:
        rows = self._db.query(TodoModel).all()
        return [self._to_schema(row) for row in rows]

    def get_by_id(self, todo_id: int) -> TodoOut | None:
        row = self._db.get(TodoModel, todo_id)
        return self._to_schema(row) if row is not None else None

    def create(self, title: str) -> TodoOut:
        row = TodoModel(
            title=title,
            done=False,
            created_at=datetime.now(timezone.utc),
        )
        self._db.add(row)
        self._db.commit()
        self._db.refresh(row)
        return self._to_schema(row)

    def update(
        self,
        todo_id: int,
        title: str | None = None,
        done: bool | None = None,
    ) -> TodoOut | None:
        row = self._db.get(TodoModel, todo_id)
        if row is None:
            return None
        if title is not None:
            row.title = title
        if done is not None:
            row.done = done
        self._db.commit()
        self._db.refresh(row)
        return self._to_schema(row)

    def delete(self, todo_id: int) -> bool:
        row = self._db.get(TodoModel, todo_id)
        if row is None:
            return False
        self._db.delete(row)
        self._db.commit()
        return True

    @staticmethod
    def _to_schema(row: TodoModel) -> TodoOut:
        return TodoOut(
            id=row.id,
            title=row.title,
            done=row.done,
            created_at=row.created_at,
        )
