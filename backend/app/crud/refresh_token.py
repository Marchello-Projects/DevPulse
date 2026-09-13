import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import generate_refresh_token, hash_refresh_token
from app.models.refresh_token import RefreshToken


async def issue_refresh_token(db: AsyncSession, user_id: uuid.UUID) -> str:
    raw_token, token_hash, expires_at = generate_refresh_token()
    db.add(RefreshToken(user_id=user_id, token_hash=token_hash, expires_at=expires_at))
    await db.commit()
    return raw_token


async def get_valid_refresh_token(db: AsyncSession, raw_token: str) -> RefreshToken | None:
    token_hash = hash_refresh_token(raw_token)
    result = await db.execute(select(RefreshToken).where(RefreshToken.token_hash == token_hash))
    token = result.scalar_one_or_none()

    if token is None or token.revoked or token.expires_at < datetime.now(timezone.utc):
        return None

    return token


async def revoke_refresh_token(db: AsyncSession, token: RefreshToken) -> None:
    token.revoked = True
    await db.commit()
