from pathlib import Path

from pydantic_settings import BaseSettings

# Resolve to backend/todos.db regardless of the working directory where
# uvicorn is launched.  A relative sqlite:///./todos.db changes meaning
# when the process starts outside the backend/ directory.
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_DEFAULT_DB_URL = f"sqlite:///{_BACKEND_DIR / 'todos.db'}"


class Settings(BaseSettings):
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    cors_origins: list[str] = ["http://localhost:5173"]
    database_url: str = _DEFAULT_DB_URL

    model_config = {"env_file": ".env"}


settings = Settings()
