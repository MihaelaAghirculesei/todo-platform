"""
Pydantic schemas for Todo entity.
Request/response DTOs with validation.
"""

from pydantic import BaseModel, ConfigDict, Field, constr, field_serializer
from typing import Optional
from datetime import datetime

class TodoCreate(BaseModel):
    """Schema for creating a new todo."""
    title: constr(min_length=1, max_length=200, strip_whitespace=True) = Field(
        ...,
        description="Todo title, 1-200 characters",
        json_schema_extra={"example": "Buy groceries"},
    )

class TodoUpdate(BaseModel):
    """Schema for updating an existing todo."""
    title: Optional[constr(min_length=1, max_length=200, strip_whitespace=True)] = Field(
        None,
        description="Todo title, 1-200 characters"
    )
    done: Optional[bool] = Field(
        None,
        description="Completion status"
    )

class TodoOut(BaseModel):
    """Schema for todo response."""
    id: int = Field(..., description="Todo unique identifier")
    title: str = Field(..., description="Todo title")
    done: bool = Field(..., description="Completion status")
    created_at: datetime = Field(..., description="Creation timestamp (ISO 8601 UTC)")

    @field_serializer("created_at")
    def serialize_created_at(self, dt: datetime) -> str:
        """Serialize to ISO 8601 with explicit UTC 'Z' suffix, as required by the API contract."""
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "done": False,
                "created_at": "2026-02-12T10:30:00Z",
            }
        }
    )