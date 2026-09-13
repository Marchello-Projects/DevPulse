import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ping import PingResult


async def create_ping_result(
    db: AsyncSession,
    project_id: uuid.UUID,
    is_up: bool,
    status_code: int | None,
    response_time_ms: float | None,
    error_message: str | None,
) -> PingResult:
    ping_result = PingResult(
        project_id=project_id,
        is_up=is_up,
        status_code=status_code,
        response_time_ms=response_time_ms,
        error_message=error_message,
    )
    db.add(ping_result)
    await db.commit()
    await db.refresh(ping_result)
    return ping_result


async def get_ping_history(
    db: AsyncSession, project_id: uuid.UUID, limit: int = 50
) -> list[PingResult]:
    result = await db.execute(
        select(PingResult)
        .where(PingResult.project_id == project_id)
        .order_by(PingResult.checked_at.desc())
        .limit(limit)
    )
    return list(result.scalars().all())
