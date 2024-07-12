from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from fai_backend.dependencies import (
    get_page_template_for_logged_in_users,
    get_project_user,
)
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.framework.display import DisplayAs
from fai_backend.framework.table import ColumnFilter, DataColumn
from fai_backend.llm.service import ask_llm_question, ask_llm_raq_question
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import list_projects_request
from fai_backend.projects.schema import ProjectResponse
from fai_backend.qaf.dependencies import (
    add_answer_action,
    add_feedback_action,
    question_details_loader,
    questions_loader,
    run_llm_on_question_create_action,
)
from fai_backend.qaf.schema import QuestionDetails
from fai_backend.qaf.views import QuestionForm, ReviewDetails
from fai_backend.schema import ProjectUser, User
from fai_backend.utils import format_datetime_human_readable

router = APIRouter(
    prefix='/api',
    tags=['QAF'],
    route_class=LoggingAPIRouter,
)


@router.get('/llm-question', response_model=Any)
async def llm_question_endpoint(question: str):
    try:
        response = await ask_llm_question(question)
        return {'response': response}
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception))


@router.get('/llm-raq-question', response_model=Any)
async def llm_raq_question_endpoint(
        question: str,
        vector_collection_name: str,
):
    try:
        response = await ask_llm_raq_question(question=question, collection_name=vector_collection_name)
        return {'response': response}
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception))


@router.get('/chat', response_model=list, response_model_exclude_none=True)
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


def to_table_data(question: QuestionDetails) -> dict[str, Any]:
    return {
        'subject': question.subject,
        'errand_id': question.errand_id,
        'timestamp.created': question.timestamp.created.date(),
        'timestamp.modified': format_datetime_human_readable(question.timestamp.modified, 1),
        'tags': question.tags,
        'review_status': question.review_status,
        'link': f'/questions/{question.id}',
    }


def question_fields() -> list[dict]:
    return [
        {'key': 'subject', 'label': 'Subject'},
        {'key': 'errand_id', 'label': 'Errand ID'},
        {'key': 'tags', 'label': 'Tags'},
        {'key': 'review_status', 'label': 'Review Status'},
        {'key': 'timestamp.modified', 'label': 'Modified'},
        {'key': 'timestamp.created', 'label': 'Created'},
        {'key': 'link', 'label': '', 'link_text': 'View'},
    ]


@router.get('/questions', response_model=list, response_model_exclude_none=True)
def questions(data: list[QuestionDetails] = Depends(questions_loader),
              view=Depends(get_page_template_for_logged_in_users)):
    return view(
        [c.DataTable(
            data=data,
            columns=[
                DataColumn(
                    key='id',
                    id='id',
                    label=_('id', 'ID'),
                    hidden=True,
                ),
                DataColumn(
                    key='question.content',
                    id='question',
                    label=_('question', 'Question'),
                    display=DisplayAs.link,
                    on_click=e.GoToEvent(url='/questions/{id}'),
                    sortable=True,
                    # filter=ColumnFilter.search,
                ),
                DataColumn(
                    key='answer.content',
                    id='answer',
                    label=_('answer', 'Answer'),
                    sortable=True,
                    # filter=ColumnFilter.search,
                ),
                DataColumn(
                    key='subject',
                    label=_('subject', 'Subject'),
                    filter=ColumnFilter.search,
                    sortable=True
                ),
                DataColumn(
                    key='errand_id',
                    label=_('errand_id', 'Errand ID'),
                    filter=ColumnFilter.search,
                    sortable=True
                ),
                DataColumn(
                    key='tags',
                    label=_('tags', 'Tags'),
                    filter=ColumnFilter.multi_select,
                ),
                DataColumn(
                    key='review_status',
                    label=_('review_status', 'Review Status'),
                    filter=ColumnFilter.multi_select,
                    filter_options=[
                        ('approved', 'Approved'),
                        ('rejected', 'Rejected'),
                        ('in-progress', 'In Progress'),
                        ('closed', 'Closed'),
                        ('blocked', 'Blocked'),
                        ('open', 'Open'),
                    ],
                    sortable=True

                ),
                DataColumn(
                    key='timestamp.modified',
                    label=_('modified', 'Modified'),
                    id='modified',
                    display=DisplayAs.date,
                    sortable=True,
                ),
                DataColumn(
                    key='timestamp.created',
                    id='created',
                    label=_('created', 'Created'),
                    display=DisplayAs.date,
                    sortable=True,
                ),
            ]
        )],
        _('questions', 'Questions'),
    )


@router.get('/questions/create', response_model=list, response_model_exclude_none=True)
def create_question(
        view: Callable[[list[Any], str | None], list[Any]] = Depends(get_page_template_for_logged_in_users),
) -> list:
    return QuestionForm(view, '/api/questions/create')


@router.post('/questions/create', response_model=list, response_model_exclude_none=True)
def on_create_question(
        data: QuestionDetails = Depends(run_llm_on_question_create_action),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/questions/{data.id}'))],
        _('submit_a_question', 'Create Question'''),
    )


@router.get('/questions/{conversation_id}', response_model=list, response_model_exclude_none=True)
async def question_details(
        data: QuestionDetails = Depends(question_details_loader),
        view=Depends(get_page_template_for_logged_in_users),
        authenticated_user: ProjectUser | None = Depends(get_project_user),
) -> list:
    if not data:
        return [c.FireEvent(event=e.GoToEvent(url='/questions'))]

    return ReviewDetails(authenticated_user, data, view, meta_data=to_table_data(data), meta_fields=question_fields())


@router.post('/questions/{conversation_id}/feedback', response_model=list, response_model_exclude_none=True)
def on_submit_feedback(
        data: QuestionDetails = Depends(add_feedback_action),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/questions/{data.id}'))],
        page_title=_('submit_a_question', 'Create Question'''),
    )


@router.post('/questions/{conversation_id}/answer', response_model=list, response_model_exclude_none=True)
def on_submit_answer(
        question: QuestionDetails = Depends(add_answer_action),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/questions/{question.id}'))],
        _('submit_a_question', 'Create Question'''),
    )
