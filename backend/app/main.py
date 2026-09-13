from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.models import PingResult, Project, User


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    description=(
        "DevPulse is a monitoring service for pet projects and APIs. "
        "Add a link to your project, and DevPulse will periodically ping it "
        "and notify you if it goes down.\n\n"
        "Repository: https://github.com/Marchello-Projects/DevPulse"
    ),
    version="0.1.0",  # TODO: replace with a real versioning strategy
    contact={
        "name": "Marchello",
        "url": "https://github.com/Marchello-Projects/DevPulse",
        "email": "paskalovmarkus@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
