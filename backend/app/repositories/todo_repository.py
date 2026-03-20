import threading
from datetime import datetime, timezone

from ..schemas.todo import TodoOut


class TodoRepository:
    def __init__(self) -> None:
        self._todos: dict[int, TodoOut] = {}
        self._counter: int = 0
        self._lock = threading.Lock()

    def list_all(self) -> list[TodoOut]:
        with self._lock:
            return list(self._todos.values())

    def get_by_id(self, todo_id: int) -> TodoOut | None:
        with self._lock:
            return self._todos.get(todo_id)

    def create(self, title: str) -> TodoOut:
        with self._lock:
            self._counter += 1
            todo = TodoOut(
                id=self._counter,
                title=title,
                done=False,
                created_at=datetime.now(timezone.utc),
            )
            self._todos[todo.id] = todo
            return todo

    def update(self, todo_id: int, title: str | None = None, done: bool | None = None) -> TodoOut | None:
        with self._lock:
            todo = self._todos.get(todo_id)
            if todo is None:
                return None

            updated = todo.model_copy(
                update={k: v for k, v in {"title": title, "done": done}.items() if v is not None}
            )
            self._todos[todo_id] = updated
            return updated

    def delete(self, todo_id: int) -> bool:
        with self._lock:
            if todo_id not in self._todos:
                return False
            del self._todos[todo_id]
            return True
