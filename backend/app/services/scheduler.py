import asyncio
import logging

from app.core.config import settings
from app.db.session import AsyncSessionLocal
from app.services.ping import ping_all_active_projects

logger = logging.getLogger(__name__)


async def run_ping_scheduler() -> None:
    while True:
        try:
            async with AsyncSessionLocal() as db:
                await ping_all_active_projects(db)
        except Exception:
            logger.exception("Ping scheduler iteration failed")

        await asyncio.sleep(settings.PING_INTERVAL_SECONDS)
