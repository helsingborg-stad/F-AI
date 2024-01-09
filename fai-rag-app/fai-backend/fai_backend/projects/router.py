from typing import List

from fastapi import APIRouter, Depends, Security

from fai_backend.dependencies import get_authenticated_user
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.projects.dependencies import (
    update_project_request,
    delete_project_request,
    create_project_request,
    get_project_request,
    list_projects_request,
)
from fai_backend.projects.schema import (
    ProjectResponse,
)

router = APIRouter(
    prefix="/v1",
    tags=["Projects"],
    route_class=LoggingAPIRouter,
    dependencies=[],
)


@router.post(
    "/projects",
    response_model=ProjectResponse,
    dependencies=[Security(get_authenticated_user)],
)
async def create_project(
    created_project: ProjectResponse = Depends(create_project_request),
):
    return created_project


@router.get(
    "/projects",
    response_model=List[ProjectResponse],
    dependencies=[Security(get_authenticated_user)],
)
async def read_projects(
    projects: List[ProjectResponse] = Depends(list_projects_request),
):
    return projects


@router.get(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    dependencies=[Security(get_authenticated_user)],
)
def read_project(project: ProjectResponse = Depends(get_project_request)):
    return project


@router.put(
    "/projects/{project_id}",
    response_model=ProjectResponse,
    dependencies=[Security(get_authenticated_user)],
)
def update_project(
    updated_project: ProjectResponse = Depends(update_project_request),
):
    return updated_project


@router.delete(
    "/projects/{project_id}",
    dependencies=[Security(get_authenticated_user)],
)
async def delete_project(
    removed_project: ProjectResponse = Depends(delete_project_request),
):
    return removed_project
