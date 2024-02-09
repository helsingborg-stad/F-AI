from fastapi import APIRouter, Depends

from fai_backend.conversations.dependencies import (
    get_conversation_request,
)
from fai_backend.conversations.schema import ConversationResponse
from fai_backend.dependencies import try_get_authenticated_user
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.qaf.dependencies import create_question_request, list_questions_request
from fai_backend.qaf.schema import QuestionResponse
from fai_backend.schema import User
from fai_backend.views import page_template

router = APIRouter(
    prefix='/api',
    tags=['QAF'],
    route_class=LoggingAPIRouter,
)


@router.get('/questions/create', response_model=list, response_model_exclude_none=True)
def submit_question_view(
        authenticated_user: User | None = Depends(try_get_authenticated_user)
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    if len(authenticated_user.projects) == 0:
        return [
            c.Text(
                text=_('no_projects', 'You are not a member of any proj.. wait a mintue, how did you login? 😱'),
                class_name='bg-error text-center font-black text-3xl text-warning h-screen flex  items-center justify-center leading-relaxed',
                element='h1'
            ),
        ]

    return page_template(
        c.Form(
            submit_url='/api/questions/create',
            method='POST',
            submit_text=_('create_question_submit_button', 'Submit'),
            components=[
                c.InputField(
                    name='subject',
                    title=_('input_subject_label', 'Subject'),
                    placeholder=_('input_subject_placeholder', 'Subject'),
                    required=True,
                    html_type='text',
                ),
                c.InputField(
                    name='errand_id',
                    title=_('input_label_errand_id', 'Errand ID'),
                    placeholder=_('input_label_errand_id', 'Errand ID'),
                    html_type='text',
                ),
                c.Textarea(
                    name='question',
                    title=_('input_label_question', 'Question'),
                    placeholder=_('input_question_placeholder', 'Enter your question here'),
                    required=True,
                ),
            ],
        ),
        page_title=_('submit_a_question', 'Create Question'),
    )


@router.post('/questions/create', response_model=list, response_model_exclude_none=True)
def submit_question_handler(
        created_question: QuestionResponse = Depends(create_question_request)
) -> list:
    print(created_question)
    return page_template(
        c.Link(text='Successfully submitted question', url=f'/questions/{created_question.id}'),
        page_title=_('submit_a_question', 'Create Question'''),
    )


@router.get('/questions', response_model=list, response_model_exclude_none=True)
def questions_index_view(
        page: int | None = 1,
        authenticated_user: User | None = Depends(try_get_authenticated_user),
        questions: list[QuestionResponse] = Depends(list_questions_request),
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    return page_template(
        c.Div(components=[
            c.Div(components=[
                c.Table(
                    data=[
                        {
                            'id': question.id,
                            'subject': question.subject,
                            'link': f'/questions/{question.id}',
                        }
                        for question in questions
                    ],
                    columns=[
                        {'key': 'id', 'label': 'ID'},
                        {'key': 'subject', 'label': 'Subject'},
                        {'key': 'link', 'label': '', 'link_text': 'View'},
                    ],

                    class_name='text-base-content join-item md:table-sm lg:table-md table-auto',
                ),
            ], class_name='overflow-x-auto space-y-4'),
        ], class_name='card bg-base-100 w-full max-w-6xl'),
        page_title=_('my_questions', 'My Questions'),
    )


@router.get('/questions/{conversation_id}', response_model=list, response_model_exclude_none=True)
def question_details_view(
        authenticated_user: User | None = Depends(try_get_authenticated_user),
        conversation: ConversationResponse = Depends(get_conversation_request),
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    return page_template(
        c.Text(text='This is the questions page'),
        page_title=_('my_questions', 'My Questions') + ' - Question ID: ' + conversation.id,
    )
