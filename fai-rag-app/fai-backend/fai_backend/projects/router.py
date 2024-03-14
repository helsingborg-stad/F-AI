from fastapi import APIRouter, Depends, Security

from fai_backend.dependencies import get_authenticated_user, get_page_template_for_logged_in_users, get_project_user
from fai_backend.framework import components as c
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import (
    create_project_request,
    delete_project_request,
    get_project_request,
    get_project_service,
    list_projects_request,
    update_project_request,
)
from fai_backend.projects.schema import (
    ProjectResponse,
)
from fai_backend.projects.service import ProjectService
from fai_backend.schema import ProjectUser

router = APIRouter(
    prefix='/api',
    tags=['Projects'],
    route_class=LoggingAPIRouter,
    dependencies=[],
)


@router.post(
    '/projects',
    response_model=ProjectResponse,
    dependencies=[Security(get_authenticated_user)],
)
async def create_project(
        created_project: ProjectResponse = Depends(create_project_request),
):
    return created_project


@router.get(
    '/projects',
    response_model=list[ProjectResponse],
    dependencies=[Security(get_authenticated_user)],
)
async def read_projects(
        projects: list[ProjectResponse] = Depends(list_projects_request),
):
    return projects


@router.get('/users', response_model=list, response_model_exclude_none=True)
async def list_project_users(
        view=Depends(get_page_template_for_logged_in_users),
        project_service: ProjectService = Depends(get_project_service),
        project_user: ProjectUser = Depends(get_project_user),
) -> list:
    project = await project_service.read_project(project_user.project_id)

    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Table(
                    data=[
                        {
                            'email': user.email,
                            'role': user.role,
                        }
                        for user in project.members
                    ],
                    columns=[
                        {'key': 'email', 'label': _('email', 'Email')},
                        {'key': 'role', 'label': _('role', 'Role')},
                    ],

                    class_name='text-base-content join-item md:table-sm lg:table-md table-auto',
                ),
            ], class_name='overflow-x-auto space-y-4'),
        ], class_name='card bg-base-100 w-full max-w-6xl')],
        _('users', 'Users'),
    )


@router.get('/roles', response_model=list, response_model_exclude_none=True)
async def list_project_users(
        view=Depends(get_page_template_for_logged_in_users),
        project_service: ProjectService = Depends(get_project_service),
        project_user: ProjectUser = Depends(get_project_user),
) -> list:
    project = await project_service.read_project(project_user.project_id)

    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Table(
                    data=[
                        {

                        }
                        for role in project.roles
                    ],
                    columns=[
                        {'key': role, 'label': role}
                        for role in project.roles.keys()
                    ],

                    class_name='text-base-content join-item md:table-sm lg:table-md table-auto',
                ),
            ], class_name='overflow-x-auto space-y-4'),
        ], class_name='card bg-base-100 w-full max-w-6xl')],
        _('users', 'Users'),
    )


@router.get(
    '/projects/{project_id}',
    response_model=ProjectResponse,
    dependencies=[Security(get_authenticated_user)],
)
def read_project(project: ProjectResponse = Depends(get_project_request)):
    return project


@router.put(
    '/projects/{project_id}',
    response_model=ProjectResponse,
    dependencies=[Security(get_authenticated_user)],
)
def update_project(
        updated_project: ProjectResponse = Depends(update_project_request),
):
    return updated_project


@router.delete(
    '/projects/{project_id}',
    dependencies=[Security(get_authenticated_user)],
)
async def delete_project(
        removed_project: ProjectResponse = Depends(delete_project_request),
):
    return removed_project
