from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends, Security
from langstream import join_final_output

from fai_backend.assistant.dependencies import get_template_service
from fai_backend.assistant.form import AssistantForm
from fai_backend.assistant.models import (
    AssistantTemplate,
)
from fai_backend.assistant.schema import TemplatePayload
from fai_backend.assistant.service import AssistantFactory, AssistantTemplateStore, TemplatePayloadAdapter
from fai_backend.dependencies import (
    get_authenticated_user,
    get_page_template_for_logged_in_users,
    get_project_user,
)
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.service import FileUploadService
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.framework.display import DisplayAs
from fai_backend.framework.table import DataColumn
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import (
    get_project_request,
    get_project_service,
    list_projects_request,
    update_project_request,
)
from fai_backend.projects.schema import ProjectResponse, ProjectUpdateRequest
from fai_backend.projects.service import ProjectService
from fai_backend.schema import ProjectUser

router = APIRouter(
    prefix='/api',
    tags=['Assistant'],
    route_class=LoggingAPIRouter,
    dependencies=[],
)


@router.get(
    '/assistant/{project_id}/ask/{assistant_id}',
    summary='Ask an assistant a question.',
    dependencies=[Security(get_authenticated_user)]
)
async def ask_assistant(
        project_id: str,
        assistant_id: str,
        question: str,
        projects: list[ProjectResponse] = Depends(list_projects_request),
):
    print(f'Assistant: {project_id}/{assistant_id} - {question}')
    factory = AssistantFactory([a for p in projects for a in p.assistants if p.id == project_id])
    assistant = factory.create_assistant_stream(assistant_id)
    stream = await assistant.create()
    return await join_final_output(stream(question))


@router.get(
    '/assistant/{project_id}/template',
    summary='Get assistant templates.',
    response_model=list[AssistantTemplate],
    dependencies=[Security(get_authenticated_user)]
)
async def list_templates(
        project_id: str,
        projects: list[ProjectResponse] = Depends(list_projects_request)
):
    return [a for p in projects for a in p.assistants if p.id == project_id]


@router.post(
    '/assistant/{project_id}/template',
    summary='Create/update assistant template.',
    response_model=AssistantTemplate,
    dependencies=[Security(get_authenticated_user)]
)
async def create_template(
        template: AssistantTemplate,
        existing_project: ProjectResponse = Depends(get_project_request),
        project_service: ProjectService = Depends(get_project_service),
):
    existing_project.assistants = [a for a in existing_project.assistants if a.id != template.id]
    existing_project.assistants.append(template)
    await update_project_request(
        body=ProjectUpdateRequest(**existing_project.model_dump()),
        existing_project=existing_project,
        project_service=project_service)
    return template


@router.delete(
    '/assistant/{project_id}/template/{assistant_id}',
    summary='Delete assistant template.',
    response_model=AssistantTemplate | None,
    dependencies=[Security(get_authenticated_user)]
)
async def delete_template(
        assistant_id: str,
        existing_project: ProjectResponse = Depends(get_project_request),
        project_service: ProjectService = Depends(get_project_service)
):
    assistant = next((a for a in existing_project.assistants if a.id == assistant_id), None)
    existing_project.assistants = [a for a in existing_project.assistants if a.id != assistant_id]
    await update_project_request(
        body=ProjectUpdateRequest(**existing_project.model_dump()),
        existing_project=existing_project,
        project_service=project_service)
    return assistant


@router.get('/rest/assistants', response_model=list[TemplatePayload], response_model_exclude_none=True)
async def assistants_loader(
        project_user: ProjectUser = Depends(get_project_user),
        template_service: AssistantTemplateStore = Depends(get_template_service),
):
    return [TemplatePayloadAdapter.to_template_payload(t) for t in
            await template_service.list_assistant_templates(project_user.project_id)]


@router.get('/assistants', response_model=list, response_model_exclude_none=True)
def assistants(
        data: list[TemplatePayload] = Depends(assistants_loader),
        view=Depends(get_page_template_for_logged_in_users)
):
    return view(
        [c.DataTable(
            data=data,
            columns=[
                DataColumn(
                    key='id',
                    id='id',
                    label=_('id', 'ID'),
                    hidden=False,
                ),
                DataColumn(
                    key='name',
                    label=_('name', 'Name'),
                    display=DisplayAs.link,
                    on_click=e.GoToEvent(url='/assistants/{id}'),
                ),
                DataColumn(
                    key='model',
                    label=_('Model'),
                ),
                DataColumn(
                    key='temperature',
                    label=_('Temperature'),
                ),
                DataColumn(key='delete_label',
                           display=DisplayAs.link,
                           on_click=e.GoToEvent(url='/assistants/delete/{id}'),
                           label=_('actions', 'Actions'))
            ],
            include_view_action=False
        )],
        _('assistants', 'Assistants'),
    )


@router.get('/assistants/create', response_model=list, response_model_exclude_none=True)
async def create_assistant_view(
        view: Callable[[list[Any], str | None], list[Any]] = Depends(get_page_template_for_logged_in_users),
        file_service: FileUploadService = Depends(get_file_upload_service),
        project_user: ProjectUser = Depends(get_project_user),
) -> list:
    files = file_service.list_files(project_user.project_id)
    most_recent_collection = max(files, key=lambda file: file.upload_date).collection if files else []
    most_recent_upload_files = [file for file in files if file.collection == most_recent_collection]

    return view(
        AssistantForm('/api/assistants/create', None, [
            file.collection for file in most_recent_upload_files
        ]),
        _('Create assistant'),

    )


@router.get('/rest/assistants/{assistant_id}', response_model=TemplatePayload | None, response_model_exclude_none=True)
async def load_assistant_by_id(
        assistant_id: str,
        project_user: ProjectUser = Depends(get_project_user),
        template_service: AssistantTemplateStore = Depends(get_template_service),
) -> TemplatePayload | None:
    template = await template_service.get_assistant_template(
        project_user.project_id,
        assistant_id
    )
    return TemplatePayloadAdapter.to_template_payload(template) if template else None


@router.get('/assistants/{assistant_id}', response_model=list, response_model_exclude_none=True)
def edit_assistant(
        assistant_id: str,
        template: TemplatePayload | None = Depends(load_assistant_by_id),
        view: Callable[[list[Any], str | None], list[Any]] = Depends(get_page_template_for_logged_in_users),
        file_service: FileUploadService = Depends(get_file_upload_service),
        project_user: ProjectUser = Depends(get_project_user),
) -> list:
    files = file_service.list_files(project_user.project_id)
    most_recent_collection = max(files, key=lambda file: file.upload_date).collection if files else []
    most_recent_upload_files = [file for file in files if file.collection == most_recent_collection]

    return view(
        [c.Div(components=AssistantForm(
            f'/api/assistants/{assistant_id}', template,
            [
                file.collection for file in most_recent_upload_files
            ])),
        ],
        _('Edit assistant') + f' ({template.id})'
    ) if template else [
        c.FireEvent(event=e.GoToEvent(url='/assistants'))
    ]


# TODO: fix delete assistants hack
@router.get('/assistants/delete/{assistant_id}', response_model=list, response_model_exclude_none=True)
async def delete_assistant(assistant_id: str,
                           project_user: ProjectUser = Depends(get_project_user),
                           template_service: AssistantTemplateStore = Depends(get_template_service)) -> list:
    print(f'Delete assistant: {assistant_id}')
    await template_service.delete_assistant_template(project_user.project_id, assistant_id)
    return [c.FireEvent(event=e.GoToEvent(url='/assistants'))]


@router.post('/rest/assistants/create', response_model=TemplatePayload | None, response_model_exclude_none=True)
async def create_assistant_action(
        body: TemplatePayload,
        project_user: ProjectUser = Depends(get_project_user),
        template_service: AssistantTemplateStore = Depends(get_template_service),
) -> TemplatePayload | None:
    template = await template_service.put_assistant_template(
        project_user.project_id,
        TemplatePayloadAdapter.from_template_payload(body)
    )
    return TemplatePayloadAdapter.to_template_payload(template) if template else None


@router.post('/rest/assistants/{assistant_id}', response_model=TemplatePayload | None, response_model_exclude_none=True)
async def update_assistant_action(
        assistant_id: str,
        body: TemplatePayload,
        project_user: ProjectUser = Depends(get_project_user),
        template_service: AssistantTemplateStore = Depends(get_template_service),
) -> TemplatePayload | None:
    body.id = assistant_id
    template = await template_service.put_assistant_template(
        project_user.project_id,
        TemplatePayloadAdapter.from_template_payload(body)
    )
    return TemplatePayloadAdapter.to_template_payload(template) if template else None


@router.post('/assistants/create', response_model=list, response_model_exclude_none=True)
def on_create_assistant(
        data: TemplatePayload = Depends(create_assistant_action),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/assistants/{data.id}'))],
        _('Create assistant')
    )


@router.post('/assistants/{assistant_id}', response_model=list, response_model_exclude_none=True)
def on_update_assistant(
        data: TemplatePayload = Depends(update_assistant_action),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/assistants/{data.id}'))],
        _('Edit assistant') + f' ({data.id})'
    )
