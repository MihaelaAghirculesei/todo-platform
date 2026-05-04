from ..exceptions import InvalidTitleError, NotFoundError
from ..repositories.todo_repository import TodoRepository
from ..schemas.todo import TodoCreate, TodoOut, TodoUpdate

_TITLE_MAX_LENGTH = 200


def _validate_title(title: str) -> str:
    title = title.strip()
    if not title:
        raise InvalidTitleError("Title must not be empty")
    if len(title) > _TITLE_MAX_LENGTH:
        raise InvalidTitleError(f"Title must be at most {_TITLE_MAX_LENGTH} characters")
    return title


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
        title = _validate_title(payload.title)
        return self._repo.create(title)

    def update(self, todo_id: int, payload: TodoUpdate) -> TodoOut:
        title = _validate_title(payload.title) if payload.title is not None else None
        updated = self._repo.update(todo_id, title=title, done=payload.done)
        if updated is None:
            raise NotFoundError(f"Todo {todo_id} not found")
        return updated

    def delete(self, todo_id: int) -> None:
        if not self._repo.delete(todo_id):
            raise NotFoundError(f"Todo {todo_id} not found")
