from fastapi import APIRouter, Depends
from pydantic import BaseModel

from fai_backend.conversations.dependencies import (
    create_conversation_request,
    get_conversation_request,
    list_conversations_request,
)
from fai_backend.conversations.schema import ConversationResponse
from fai_backend.dependencies import try_get_authenticated_user
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
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
                    name='metadata.subject',
                    title=_('input_subject_label', 'Subject'),
                    placeholder=_('input_subject_placeholder', 'Subject'),
                    required=True,
                    html_type='text',
                ),
                c.InputField(
                    name='project_id',
                    html_type='hidden',
                    value=authenticated_user.projects[0].project_id,
                ),
                c.InputField(
                    name='metadata.errand_id',
                    title=_('input_label_errand_id', 'Errand ID'),
                    placeholder=_('input_label_errand_id', 'Errand ID'),
                    html_type='text',
                ),
                c.Textarea(
                    name='messages[0].content',
                    title=_('input_email_label', 'Email'),
                    placeholder=_('input_question_placeholder', 'Enter your question here'),
                    required=True,
                ),
            ],
        ),
        page_title=_('submit_a_question', 'Create Question'),
    )


class QuestionResponse(BaseModel):
    id: str
    errand_id: str
    subject: str
    question: str
    answer: str
    created_by: str


def create_question_request(
        created_conversation: ConversationResponse = Depends(create_conversation_request)
) -> QuestionResponse:
    return QuestionResponse(
        id=created_conversation.id,
        errand_id=created_conversation.metadata.get('errand_id'),
        subject=created_conversation.metadata.get('subject'),
        question=created_conversation.messages[0].content,
        answer='',
        created_by=created_conversation.created_by,
    )


@router.post('/questions/create', response_model=list, response_model_exclude_none=True)
def submit_question_handler(
        created_question: QuestionResponse = Depends(create_question_request)

) -> list:
    return page_template(
        c.Link(text='Successfully submitted question', url=f'/questions/{created_question.id}'),
        page_title=_('submit_a_question', 'Create Question'''),
    )


@router.get('/questions', response_model=list, response_model_exclude_none=True)
def questions_index_view(
        authenticated_user: User | None = Depends(try_get_authenticated_user),
        conversations: list[ConversationResponse] = Depends(list_conversations_request),
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    return page_template(
        c.Div(components=[
            c.Div(components=[
                c.Table(
                    data=[
                        {
                            'id': conversation.id,
                            'subject': conversation.metadata.get('subject'),
                            'link': f'/questions/{conversation.id}',
                        }
                        for conversation in conversations
                    ],
                    columns=[
                        {'key': 'id', 'label': 'ID'},
                        {'key': 'subject', 'label': 'Subject'},
                        {'key': 'link', 'label': '', 'link_text': 'View'},
                    ],
                    row_class='border-neutral',
                    header_class='bg-base-200 join-item p-20 h-16'
                ),

            ], class_name='card-body py-4 px-0 pt-0'),
        ], class_name='card border border-base-200 min-h-96 h-[66vh] join w-full max-w-[80%]'),
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
