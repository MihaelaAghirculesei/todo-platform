from ..exceptions import NotFoundError
from ..repositories.todo_repository import TodoRepository
from ..schemas.todo import TodoCreate, TodoOut, TodoUpdate


class TodoService:
    def __init__(self, repository: TodoRepository) -> None:
        self._repo = repository

    def get_all(self) -> list[TodoOut]:
        return self._repo.list_all()

    def get_by_id(self, todo_id: int) -> TodoOut:
        todo = self._repo.get_by_id(todo_id)
        if todo is None:
            raise NotFoundError(f"Todo {todo_id} not found")
        return todo

    def create(self, payload: TodoCreate) -> TodoOut:
        return self._repo.create(payload.title)

    def update(self, todo_id: int, payload: TodoUpdate) -> TodoOut:
        updated = self._repo.update(todo_id, title=payload.title, done=payload.done)
        if updated is None:
            raise NotFoundError(f"Todo {todo_id} not found")
        return updated

    def delete(self, todo_id: int) -> None:
        if not self._repo.delete(todo_id):
            raise NotFoundError(f"Todo {todo_id} not found")
