import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models import TodoModel  # noqa: F401 — registers model with Base.metadata
from app.repositories.todo_repository import TodoRepository
from app.services.todo_service import TodoService

_TEST_ENGINE = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_TEST_ENGINE)

Base.metadata.create_all(bind=_TEST_ENGINE)


@pytest.fixture()
def db_session():
    db = _TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        with _TEST_ENGINE.begin() as conn:
            for table in reversed(Base.metadata.sorted_tables):
                conn.execute(table.delete())


@pytest.fixture()
def repository(db_session):
    return TodoRepository(db_session)


@pytest.fixture()
def service(repository):
    return TodoService(repository)


@pytest.fixture()
def client(db_session):
    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
