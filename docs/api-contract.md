# API Contract – Todo Platform

This document defines the interface between backend and frontend.
Both sides must follow this contract exactly.

---

## Base URL

Local: http://localhost:8000
Production: https://todo-aghirculesei.onrender.com

---

## Data Model: Todo

A Todo object contains the following fields:

- id: number (unique identifier)
- title: string
- done: boolean
- created_at: string (ISO date)

Example:
{
  "id": 1,
  "title": "Buy milk",
  "done": false,
  "created_at": "2026-01-01T10:00:00Z"
}

---

## Endpoints

### GET /health
Purpose:
Check if the backend is running. HEAD is accepted too, for uptime monitors.

Response:
{
  "status": "ok"
}

---

### GET /todos
Purpose:
Return a list of all todos.

Response:
[
  {
    "id": 1,
    "title": "Buy milk",
    "done": false,
    "created_at": "2026-01-01T10:00:00Z"
  }
]

---

### POST /todos
Purpose:
Create a new todo.

Request:
{
  "title": "Buy milk"
}

Response:
{
  "id": 1,
  "title": "Buy milk",
  "done": false,
  "created_at": "2026-01-01T10:00:00Z"
}

---

### PATCH /todos/{id}
Purpose:
Update an existing todo.

Request (both fields are optional; only the fields sent are updated):
{
  "title": "Buy bread",
  "done": true
}

Response:
Updated Todo object.

---

### DELETE /todos/{id}
Purpose:
Delete a todo.

Response:
No content.

---

## Status Codes

| Endpoint | Success | Errors |
|---|---|---|
| GET, HEAD /health | 200 OK | – |
| GET /todos | 200 OK | – |
| POST /todos | 201 Created | 400 |
| PATCH /todos/{id} | 200 OK | 400, 404 |
| DELETE /todos/{id} | 204 No Content | 400, 404 |

- 400 Bad Request: invalid input, e.g. an empty or whitespace-only title, a title longer than 200 characters, a missing or wrongly typed field, or an id that is not a positive integer. Request validation errors are returned as 400 instead of FastAPI's default 422, so clients handle a single status code for bad input.
- 404 Not Found: no todo exists with the given id.

---

## Error Format

Every error response has the same shape:

{
  "detail": "Todo 999 not found"
}
