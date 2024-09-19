from fastapi import APIRouter, Depends

from fai_backend.assistant.chat_state import ChatStateService, get_chat_state_service
from fai_backend.dependencies import get_page_template_for_logged_in_users, get_project_user
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.framework.display import DisplayAs
from fai_backend.framework.table import DataColumn
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import list_projects_request
from fai_backend.projects.schema import ProjectResponse
from fai_backend.schema import User, ProjectUser

router = APIRouter(
    prefix='/api',
    tags=['NewChat'],
    route_class=LoggingAPIRouter,
)


@router.get('/chat', response_model=list, response_model_exclude_none=True)
def chat_index_view(authenticated_user: User | None = Depends(get_project_user),
                    view=Depends(get_page_template_for_logged_in_users),
                    projects: list[ProjectResponse] = Depends(list_projects_request)) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    assistants = [c.Assistant(id=a.id,
                              name=a.meta.name,
                              project=p.id,
                              description=a.meta.description,
                              sampleQuestions=a.meta.sample_questions) for p in projects for a in p.assistants]

    return view([c.SSEChat(assistants=assistants)],
                _('chat', 'Chat'))


@router.get('/chat/history', response_model=list, response_model_exclude_none=True)
async def chat_history_view(
        view=Depends(get_page_template_for_logged_in_users),
        chat_state_service: ChatStateService = Depends(get_chat_state_service),
        user: ProjectUser = Depends(get_project_user),
) -> list:
    states = await chat_state_service.get_states(user=user.email)
    return view(
        [c.DataTable(data=states,
                     columns=[DataColumn(key='title',
                                         id='title',
                                         display=DisplayAs.link,
                                         on_click=e.GoToEvent(url='/chat/{chat_id}'),
                                         sortable=True,
                                         label=_('title', 'Title'))])],
        _('chat_history', 'History')
    )
