import pytest

from app.exceptions import InvalidTitleError, NotFoundError
from app.schemas.todo import TodoCreate, TodoUpdate

class TestCreateTodo:
    def test_create_valid(self, service):
        payload = TodoCreate(title="Buy milk")

        result = service.create(payload)

        assert result.id == 1
        assert result.title == "Buy milk"
        assert result.done is False
        assert result.created_at is not None

    def test_create_trims_whitespace(self, service):
        result = service.create(TodoCreate(title="  Buy milk  "))

        assert result.title == "Buy milk"

    def test_create_empty_title_rejected(self, service):
        with pytest.raises(InvalidTitleError):
            service.create(TodoCreate(title=""))

    def test_create_whitespace_only_title_rejected(self, service):
        with pytest.raises(InvalidTitleError):
            service.create(TodoCreate(title="   "))

    def test_create_title_too_long_rejected(self, service):
        with pytest.raises(InvalidTitleError):
            service.create(TodoCreate(title="a" * 201))

    def test_create_increments_id(self, service):
        first = service.create(TodoCreate(title="First"))
        second = service.create(TodoCreate(title="Second"))

        assert first.id == 1
        assert second.id == 2


class TestGetByIdTodo:
    def test_get_by_id_returns_todo(self, service):
        created = service.create(TodoCreate(title="Task"))

        result = service.get_by_id(created.id)

        assert result.id == created.id
        assert result.title == "Task"

    def test_get_by_id_invalid_id_raises_not_found(self, service):
        with pytest.raises(NotFoundError):
            service.get_by_id(999)


class TestUpdateTodo:
    def test_toggle_done(self, service):
        created = service.create(TodoCreate(title="Task"))

        updated = service.update(created.id, TodoUpdate(done=True))

        assert updated.done is True
        assert updated.title == "Task"

    def test_update_title(self, service):
        created = service.create(TodoCreate(title="Old"))

        updated = service.update(created.id, TodoUpdate(title="New"))

        assert updated.title == "New"
        assert updated.done is False

    def test_update_invalid_id_raises_not_found(self, service):
        with pytest.raises(NotFoundError):
            service.update(999, TodoUpdate(done=True))

class TestDeleteTodo:
    def test_delete_existing(self, service):
        created = service.create(TodoCreate(title="Task"))

        service.delete(created.id)

        assert service.get_all() == []

    def test_delete_invalid_id_raises_not_found(self, service):
        with pytest.raises(NotFoundError):
            service.delete(999)