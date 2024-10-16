from typing import Any, Callable

from fastapi import APIRouter, Depends

from fai_backend.dependencies import get_page_template_for_logged_in_users, get_project_user
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.new_chat.dependencies import get_chat_state_service
from fai_backend.new_chat.service import ChatStateService
from fai_backend.new_chat.models import ChatHistoryEditPayload
from fai_backend.new_chat.views import chat_history_edit_view, chat_history_list_view
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
                              sampleQuestions=a.meta.sample_questions) for p in projects for a in p.assistants if
                  not a.id.startswith('_')]

    return view([c.SSEChat(assistants=assistants)],
                _('chat', 'Chat'))


@router.get('/chat/history', response_model=list, response_model_exclude_none=True)
async def chat_history_view(view=Depends(get_page_template_for_logged_in_users),
                            chat_state_service: ChatStateService = Depends(get_chat_state_service),
                            user: ProjectUser = Depends(get_project_user)) -> list:
    if not user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    states = await chat_state_service.get_states(user=user.email)
    return await chat_history_list_view(view, states)


@router.get('/chat/{chat_id}', response_model=list, response_model_exclude_none=True)
async def chat_view(chat_id: str,
                    view=Depends(get_page_template_for_logged_in_users),
                    chat_state_service: ChatStateService = Depends(get_chat_state_service),
                    project_user: ProjectUser = Depends(get_project_user)) -> list:
    chat_history = await chat_state_service.get_state(chat_id)

    if chat_history is None or chat_history.user != project_user.email:
        return [c.FireEvent(event=e.GoToEvent(url='/logout'))]

    return view([c.SSEChat(chat_initial_state=chat_history)],
                _('chat_history', f'Chat history ({chat_history.title})'))


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


@router.get('/chat/edit/{chat_id}', response_model=list, response_model_exclude_none=True)
async def chat_edit(chat_id: str,
                    chat_state_service: ChatStateService = Depends(get_chat_state_service),
                    project_user: ProjectUser = Depends(get_project_user),
                    view: Callable[[list[Any], str | None], list[Any]] = Depends(
                        get_page_template_for_logged_in_users)) -> list:
    state = await chat_state_service.get_state(chat_id)
    if state is None or state.user != project_user.email:
        return [c.FireEvent(event=e.GoToEvent(url='/logout'))]

    return await chat_history_edit_view(view, state, '/api/chat/edit')


@router.patch('/chat/edit', response_model=list, response_model_exclude_none=True)
async def chat_edit_patch(data: ChatHistoryEditPayload,
                          chat_state_service: ChatStateService = Depends(get_chat_state_service)) -> list:
    old_state = await chat_state_service.get_state(data.chat_id)
    updated_state = old_state.model_copy(update={'title': data.title}, deep=True)
    await chat_state_service.update_state(data.chat_id, updated_state)

    return [c.FireEvent(event=e.GoToEvent(url='/chat/history'))]
