import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.crud.ping import get_ping_history
from app.crud.project import (
    create_project,
    delete_project,
    get_project,
    get_projects_for_owner,
    update_project,
)
from app.db.session import get_db
from app.models.ping import PingResult
from app.models.project import Project
from app.models.user import User
from app.schemas.ping import PingResultRead
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


async def _get_owned_project(
    project_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    project = await get_project(db, project_id)
    # 404, not 403, for someone else's project - a 403 would confirm the
    # project exists, leaking its presence to users who don't own it.
    if project is None or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.get("", response_model=list[ProjectRead])
async def list_projects(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Project]:
    return await get_projects_for_owner(db, current_user.id)


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project_endpoint(
    project_in: ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Project:
    return await create_project(db, current_user.id, project_in)


@router.get("/{project_id}", response_model=ProjectRead)
async def read_project(project: Project = Depends(_get_owned_project)) -> Project:
    return project


@router.patch("/{project_id}", response_model=ProjectRead)
async def update_project_endpoint(
    project_in: ProjectUpdate,
    project: Project = Depends(_get_owned_project),
    db: AsyncSession = Depends(get_db),
) -> Project:
    return await update_project(db, project, project_in)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_endpoint(
    project: Project = Depends(_get_owned_project),
    db: AsyncSession = Depends(get_db),
) -> None:
    await delete_project(db, project)


@router.get("/{project_id}/pings", response_model=list[PingResultRead])
async def list_project_pings(
    project: Project = Depends(_get_owned_project),
    db: AsyncSession = Depends(get_db),
) -> list[PingResult]:
    return await get_ping_history(db, project.id)
