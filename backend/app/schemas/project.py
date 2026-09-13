import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    url: HttpUrl


class ProjectCreate(ProjectBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"name": "My Pet API", "url": "https://myapi.example.com/health"}]
        }
    )


class ProjectUpdate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"name": "My Pet API", "url": "https://myapi.example.com/health", "is_active": False}]
        }
    )

    name: str | None = Field(default=None, min_length=1, max_length=255)
    url: HttpUrl | None = None
    is_active: bool | None = None


class ProjectRead(ProjectBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "owner_id": "9c858901-8a57-4791-81fe-4c455b099bc9",
                    "name": "My Pet API",
                    "url": "https://myapi.example.com/health",
                    "is_active": True,
                    "created_at": "2026-09-13T18:00:00Z",
                }
            ]
        },
    )

    id: uuid.UUID
    owner_id: uuid.UUID
    is_active: bool
    created_at: datetime
