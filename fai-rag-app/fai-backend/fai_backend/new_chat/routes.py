from fastapi import APIRouter, Depends

from fai_backend.dependencies import get_page_template_for_logged_in_users, get_project_user
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.phrase import phrase as _
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.projects.dependencies import list_projects_request
from fai_backend.projects.schema import ProjectResponse
from fai_backend.schema import User

router = APIRouter(
    prefix='/api',
    tags=['NewChat'],
    route_class=LoggingAPIRouter,
)


@router.get('/view/chat', response_model=list, response_model_exclude_none=True)
def chat_index_view(
        authenticated_user: User | None = Depends(get_project_user),
        view=Depends(get_page_template_for_logged_in_users),
        projects: list[ProjectResponse] = Depends(list_projects_request),
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    assistants = [c.Assistant(
        id=a.id,
        name=a.meta.name,
        project=p.id,
        description=a.meta.description,
        sampleQuestions=a.meta.sample_questions
    ) for p in projects for a in p.assistants]

    return view(
        [c.SSEChat(
            assistants=assistants,
            endpoint='/api/assistant-stream'
        )],
        _('chat', 'Chat'),
    )
