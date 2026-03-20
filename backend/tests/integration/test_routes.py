import re

# ISO 8601 UTC: e.g. "2026-02-12T10:30:00Z"
_ISO_8601_UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")


class TestHealthEndpoint:
    def test_health_returns_ok(self, client):
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestTodosEndpoints:
    def test_get_todos_empty(self, client):
        response = client.get("/todos")

        assert response.status_code == 200
        assert response.json() == []

    def test_create_then_get_returns_created_item(self, client):
        create_response = client.post("/todos", json={"title": "Buy milk"})

        assert create_response.status_code == 201
        created = create_response.json()
        assert created["title"] == "Buy milk"
        assert created["done"] is False
        assert "id" in created
        assert _ISO_8601_UTC.match(created["created_at"]), (
            f"created_at must be ISO 8601 UTC (e.g. '2026-02-12T10:30:00Z'), got: {created['created_at']!r}"
        )

        list_response = client.get("/todos")
        todos = list_response.json()

        assert len(todos) == 1
        assert todos[0]["id"] == created["id"]

    def test_create_invalid_title_returns_400(self, client):
        response = client.post("/todos", json={"title": ""})

        assert response.status_code == 400

    def test_patch_updates_done(self, client):
        create_response = client.post("/todos", json={"title": "Task"})
        todo_id = create_response.json()["id"]

        patch_response = client.patch(f"/todos/{todo_id}", json={"done": True})

        assert patch_response.status_code == 200
        assert patch_response.json()["done"] is True
        assert patch_response.json()["title"] == "Task"

    def test_patch_nonexistent_returns_404(self, client):
        response = client.patch("/todos/999", json={"done": True})

        assert response.status_code == 404

    def test_delete_removes_item(self, client):
        create_response = client.post("/todos", json={"title": "Task"})
        todo_id = create_response.json()["id"]

        delete_response = client.delete(f"/todos/{todo_id}")

        assert delete_response.status_code == 204

        list_response = client.get("/todos")
        assert list_response.json() == []

    def test_delete_nonexistent_returns_404(self, client):
        response = client.delete("/todos/999")

        assert response.status_code == 404

    def test_patch_negative_id_returns_400(self, client):
        response = client.patch("/todos/-1", json={"done": True})

        assert response.status_code == 400

    def test_delete_negative_id_returns_400(self, client):
        response = client.delete("/todos/-1")

        assert response.status_code == 400
