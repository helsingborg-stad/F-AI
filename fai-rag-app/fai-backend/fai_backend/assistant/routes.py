from fastapi import APIRouter, Depends
from langstream import join_final_output

from fai_backend.assistant.service import AssistantFactory
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.projects.dependencies import list_projects_request
from fai_backend.projects.schema import ProjectResponse

router = APIRouter(
    prefix='/api',
    tags=['Assistant'],
    route_class=LoggingAPIRouter,
    dependencies=[],
)


@router.get(
    '/assistant/{project_id}/{assistant_id}',
    # dependencies=[Security(get_authenticated_user)]
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
