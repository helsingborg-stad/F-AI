from collections.abc import Callable
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Request

from fai_backend.dependencies import (
    get_authenticated_user,
    get_page_template_for_logged_in_users,
    get_project_user,
)
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.service import FileUploadService
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.llm.service import ask_llm_question, ask_llm_raq_question
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.qaf.dependencies import (
    list_questions_filter_params,
    list_submitted_questions_request,
    submit_answer_request,
    submit_feedback_request,
    submit_question_and_generate_answer_request,
    submitted_question_details_request,
)
from fai_backend.qaf.schema import QuestionDetails, QuestionFilterParams
from fai_backend.qaf.views import question_form, review_details, table_index
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
        file_service: FileUploadService = Depends(get_file_upload_service),
        authenticated_user: User | None = Depends(get_project_user),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    documents = [{'id': doc.collection, 'name': doc.file_name} for doc in
                 file_service.list_files(authenticated_user.project_id)]

    return view(
        [c.SSEChat(
            documents=documents,
            endpoint='/api/chat-stream'
        )],
        _('chat', 'Chat'),
    )


@router.get('/questions', response_model=list, response_model_exclude_none=True)
def reviews_index_view(
        questions: list[QuestionDetails] = Depends(list_submitted_questions_request),
        view=Depends(get_page_template_for_logged_in_users),
        query_params: QuestionFilterParams = Depends(list_questions_filter_params),
        request: Request = None,
) -> list:
    return table_index(
        data=[
            {
                'subject': question.subject,
                'errand_id': question.errand_id,
                'timestamp.created': question.timestamp.created.date(),
                'timestamp.modified': format_datetime_human_readable(question.timestamp.modified, 1),
                'tags': question.tags,
                'status': question.status,
                'review_status': question.review_status,
                'link': f'/questions/{question.id}',
            }
            for question in questions
        ],
        columns=[
            {'key': 'subject', 'label': 'Subject'},
            {'key': 'errand_id', 'label': 'Errand ID'},
            {'key': 'status', 'label': 'Status'},
            {'key': 'timestamp.modified', 'label': 'Modified'},
            {'key': 'timestamp.created', 'label': 'Created'},
            {'key': 'review_status', 'label': 'Review Status'},
            {'key': 'link', 'label': '', 'link_text': 'View'},
        ],
        query_params=query_params.model_dump(exclude_none=True),
        view=view,
    )


@router.get('/questions/create', response_model=list, response_model_exclude_none=True)
def create_question_view(
        view: Callable[[list[Any], str | None], list[Any]] = Depends(get_page_template_for_logged_in_users),
        authenticated_user: User = Depends(get_authenticated_user)
) -> list:
    if len(authenticated_user.projects) == 0:
        return [
            c.Text(
                text=_('no_projects', 'You are not a member of any proj.. wait a mintue, how did you login? 😱'),
                class_name='bg-error text-center font-black text-3xl text-warning h-screen flex items-center justify-center leading-relaxed',
                element='h1'
            ),
        ]

    return question_form(view, '/api/questions/create')


@router.post('/questions/create', response_model=list, response_model_exclude_none=True)
def create_question_handler(
        question: QuestionDetails = Depends(submit_question_and_generate_answer_request),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/questions/{question.id}'))],
        _('submit_a_question', 'Create Question'''),
    )


@router.get('/questions/{conversation_id}', response_model=list, response_model_exclude_none=True)
async def question_details_view(
        authenticated_user: ProjectUser | None = Depends(get_project_user),
        question: QuestionDetails = Depends(submitted_question_details_request),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    if not question:
        return [c.FireEvent(event=e.GoToEvent(url='/questions'))]

    return review_details(authenticated_user, question, view)


@router.post('/questions/{conversation_id}/feedback', response_model=list, response_model_exclude_none=True)
def submit_feedback_handler(
        conversation_id: str,
        review: QuestionDetails = Depends(submit_feedback_request),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/questions/{review.id}'))],
        page_title=_('submit_a_question', 'Create Question'''),
    )


@router.post('/questions/{conversation_id}/answer', response_model=list, response_model_exclude_none=True)
def submit_answer_handler(
        question: QuestionDetails = Depends(submit_answer_request),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/questions/{question.id}'))],
        _('submit_a_question', 'Create Question'''),
    )
