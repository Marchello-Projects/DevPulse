import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PingResultRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "id": "6f9619ff-8b86-d011-b42d-00cf4fc964ff",
                    "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    "is_up": True,
                    "status_code": 200,
                    "response_time_ms": 84.3,
                    "error_message": None,
                    "checked_at": "2026-09-13T18:00:00Z",
                }
            ]
        },
    )

    id: uuid.UUID
    project_id: uuid.UUID
    is_up: bool
    status_code: int | None
    response_time_ms: float | None
    error_message: str | None
    checked_at: datetime
