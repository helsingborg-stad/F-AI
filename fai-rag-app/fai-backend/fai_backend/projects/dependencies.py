from fastapi import Depends, HTTPException

from fai_backend.projects.schema import (
    ProjectCreateRequest,
    ProjectResponse,
    ProjectUpdateRequest,
)
from fai_backend.projects.service import ProjectService
from fai_backend.repositories import projects_repo


def get_project_service() -> ProjectService:
    return ProjectService(projects_repo)


async def get_project_request(
        project_id: str, projects_service: ProjectService = Depends(get_project_service)
) -> ProjectResponse:
    project = await projects_service.read_project(project_id)
    if not project:
        HTTPException(status_code=404, detail='Project not found')
    return ProjectResponse.model_validate(project.model_dump())


async def update_project_request(
        body: ProjectUpdateRequest,
        existing_project: ProjectResponse = Depends(get_project_request),
        project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return await project_service.update_project(existing_project.id, body)


async def delete_project_request(
        existing_project: ProjectResponse = Depends(get_project_request),
        project_service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    return await project_service.delete_project(existing_project.id)


async def create_project_request(
        body: ProjectCreateRequest,
        service: ProjectService = Depends(get_project_service),
) -> ProjectResponse:
    created_project = await service.create_project(body)
    response = ProjectResponse.model_validate(created_project.model_dump())

    return response


async def list_projects_request(
        skip: int = 0,
        limit: int = 100,
        service: ProjectService = Depends(get_project_service),
) -> list[ProjectResponse]:
    projects = await service.read_projects(skip, limit)
    return [
        ProjectResponse.model_validate(project.model_dump()) for project in projects
    ]
