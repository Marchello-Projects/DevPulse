import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


async def get_project(db: AsyncSession, project_id: uuid.UUID) -> Project | None:
    return await db.get(Project, project_id)


async def get_projects_for_owner(db: AsyncSession, owner_id: uuid.UUID) -> list[Project]:
    result = await db.execute(
        select(Project).where(Project.owner_id == owner_id).order_by(Project.created_at)
    )
    return list(result.scalars().all())


async def create_project(
    db: AsyncSession, owner_id: uuid.UUID, project_in: ProjectCreate
) -> Project:
    project = Project(owner_id=owner_id, name=project_in.name, url=str(project_in.url))
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def update_project(
    db: AsyncSession, project: Project, project_in: ProjectUpdate
) -> Project:
    for field, value in project_in.model_dump(exclude_unset=True).items():
        setattr(project, field, str(value) if field == "url" else value)
    await db.commit()
    await db.refresh(project)
    return project


async def delete_project(db: AsyncSession, project: Project) -> None:
    await db.delete(project)
    await db.commit()
