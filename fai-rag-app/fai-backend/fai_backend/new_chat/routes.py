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
from fai_backend.schema import ProjectUser

router = APIRouter(
    prefix='/api',
    tags=['NewChat'],
    route_class=LoggingAPIRouter,
)


@router.get('/chat', response_model=list, response_model_exclude_none=True)
def chat_index_view(authenticated_user: ProjectUser | None = Depends(get_project_user),
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
async def chat_history_view(view=Depends(get_page_template_for_logged_in_users),
                            chat_state_service: ChatStateService = Depends(get_chat_state_service),
                            user: ProjectUser = Depends(get_project_user)) -> list:

    if not user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    states = await chat_state_service.get_states(user=user.email)
    return view(
        [c.DataTable(data=states,
                     columns=[DataColumn(key='title',
                                         id='title',
                                         display=DisplayAs.link,
                                         on_click=e.GoToEvent(url='/chat/{chat_id}'),
                                         sortable=True,
                                         label=_('title', 'Title')),
                              DataColumn(key='delete_label',
                                         display=DisplayAs.link,
                                         on_click=e.GoToEvent(url='/chat/delete/{chat_id}'),
                                         label=_('actions', 'Actions'))],
                     include_view_action=False)],
        _('chat_history', 'Chat history')
    )


@router.get('/chat/{chat_id}', response_model=list, response_model_exclude_none=True)
async def chat_view(chat_id: str,
                    view=Depends(get_page_template_for_logged_in_users),
                    chat_state_service: ChatStateService = Depends(get_chat_state_service),
                    project_user: ProjectUser = Depends(get_project_user)) -> list:

    chat_history = await chat_state_service.get_state(chat_id)

    if chat_history is None or chat_history.user != project_user.email:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    chat_history.history = [h for h in chat_history.history if h.source == 'user' or h.source == 'assistant']

    return view([c.SSEChat(chat_initial_state=chat_history)],
                _('chat_history', 'Chat history'))


@router.get('/chat/delete/{chat_id}', response_model=list, response_model_exclude_none=True)
async def chat_delete(chat_id: str,
                      chat_state_service: ChatStateService = Depends(get_chat_state_service),
                      project_user: ProjectUser = Depends(get_project_user)) -> list:

    chat_history = await chat_state_service.get_state(chat_id)
    if chat_history is None or chat_history.user != project_user.email:
        return [c.FireEvent(event=e.GoToEvent(url='/chat/history'))]

    await chat_state_service.delete_state(chat_id)
    print(f'Chat history: {chat_id} deleted')
    return [c.FireEvent(event=e.GoToEvent(url='/chat/history'))]
