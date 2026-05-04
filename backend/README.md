# Backend – Todo Platform API

REST API built with FastAPI. Provides CRUD operations for managing todos.

## Tech Stack

- Python 3.12+
- FastAPI
- Pydantic v2
- SQLAlchemy 2.0 + SQLite

## Setup

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate      
pip install -r requirements.txt
```

Copy the environment file and adjust if needed:

```bash
cp .env.example .env
```

## Run Dev Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API available at `http://localhost:8000`

## Run Tests

```bash
pytest
```

With verbose output:

```bash
pytest -v
```

## API Endpoints

| Method | Path            | Description       |
|--------|-----------------|-------------------|
| GET    | /health         | Health check      |
| GET    | /todos          | List all todos    |
| POST   | /todos          | Create a todo     |
| PATCH  | /todos/{id}     | Update a todo     |
| DELETE | /todos/{id}     | Delete a todo     |

See [docs/api-contract.md](../docs/api-contract.md) for the full API contract.

## Contributors

- [MihaelaAghirculesei](https://github.com/MihaelaAghirculesei)
- [AlSweidanAhmad](https://github.com/AlSweidanAhmad)

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── dependencies.py    # Dependency injection
│   │   ├── router.py          # Route aggregation
│   │   └── routes/
│   │       ├── health.py      # GET /health
│   │       └── todos.py       # CRUD /todos
│   ├── core/
│   │   └── config.py          # App settings (database_url, cors, …)
│   ├── db/
│   │   ├── base.py            # SQLAlchemy DeclarativeBase
│   │   └── session.py         # engine, SessionLocal, get_db
│   ├── models/
│   │   └── todo_model.py      # SQLAlchemy ORM model
│   ├── repositories/
│   │   └── todo_repository.py # SQLAlchemy data access layer
│   ├── schemas/
│   │   └── todo.py            # Pydantic DTOs
│   └── services/
│       └── todo_service.py    # Business logic
└── tests/
    ├── conftest.py            # Shared fixtures (SQLite in-memory)
    ├── unit/
    │   └── test_todo_service.py
    └── integration/
        └── test_routes.py
```
