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
Check if the backend is running.

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

Request:
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
