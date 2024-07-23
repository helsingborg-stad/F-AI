from fastapi import APIRouter, Depends, Security
from langstream import join_final_output

from fai_llm.assistant.models import AssistantTemplate
from fai_llm.assistant.service import AssistantFactory
from fai_llm.dependencies import get_authenticated_user
from fai_llm.logger.route_class import APIRouter as LoggingAPIRouter
from fai_llm.projects.dependencies import list_projects_request, get_project_request, get_project_service, \
    update_project_request
from fai_llm.projects.schema import ProjectResponse, ProjectUpdateRequest
from fai_llm.projects.service import ProjectService

router = APIRouter(
    prefix='/api',
    tags=['Assistant'],
    route_class=LoggingAPIRouter,
    dependencies=[],
)


@router.get(
    '/assistant/{project_id}/ask/{assistant_id}',
    summary="Ask an assistant a question.",
    dependencies=[Security(get_authenticated_user)]
)
async def ask_assistant(
        project_id: str,
        assistant_id: str,
        question: str,
        projects: list[ProjectResponse] = Depends(list_projects_request),
):
    print(f"Assistant: {project_id}/{assistant_id} - {question}")
    factory = AssistantFactory([a for p in projects for a in p.assistants if p.id == project_id])
    assistant = factory.create_assistant_stream(assistant_id)
    stream = await assistant.create()
    return await join_final_output(stream(question))


@router.get(
    '/assistant/{project_id}/template',
    summary="Get assistant templates.",
    response_model=list[AssistantTemplate],
    dependencies=[Security(get_authenticated_user)]
)
async def get_template(
        project_id: str,
        projects: list[ProjectResponse] = Depends(list_projects_request)
):
    return [a for p in projects for a in p.assistants if p.id == project_id]


@router.post(
    '/assistant/{project_id}/template',
    summary="Create/update assistant template.",
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
    summary="Delete assistant template.",
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
