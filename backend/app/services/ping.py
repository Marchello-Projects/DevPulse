import time

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud.ping import create_ping_result
from app.models.ping import PingResult
from app.models.project import Project


async def ping_project(db: AsyncSession, project: Project) -> PingResult:
    start = time.monotonic()
    is_up = False
    status_code: int | None = None
    error_message: str | None = None

    try:
        async with httpx.AsyncClient(
            timeout=settings.PING_TIMEOUT_SECONDS, follow_redirects=True
        ) as client:
            response = await client.get(project.url)
        status_code = response.status_code
        is_up = response.is_success
    except httpx.RequestError as exc:
        error_message = str(exc)

    response_time_ms = (time.monotonic() - start) * 1000

    return await create_ping_result(
        db,
        project_id=project.id,
        is_up=is_up,
        status_code=status_code,
        response_time_ms=response_time_ms,
        error_message=error_message,
    )


async def ping_all_active_projects(db: AsyncSession) -> None:
    result = await db.execute(select(Project).where(Project.is_active.is_(True)))
    for project in result.scalars().all():
        await ping_project(db, project)
