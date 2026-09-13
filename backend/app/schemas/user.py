import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"email": "dev@example.com", "password": "supersecret123"}]
        }
    )

    password: str = Field(min_length=8, max_length=128)


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "email": "dev@example.com",
                    "created_at": "2026-09-13T18:00:00Z",
                }
            ]
        },
    )

    id: uuid.UUID
    created_at: datetime
