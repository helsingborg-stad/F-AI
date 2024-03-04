from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from fai_backend.conversations.models import Conversation, Message
from fai_backend.dependencies import get_authenticated_user, get_project_user, try_get_authenticated_user
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.framework.components import AnyUI
from fai_backend.llm.service import ask_llm_question, ask_llm_raq_question
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.qaf.dependencies import (
    list_my_questions_request,
    my_question_details_request,
    submit_answer_request,
    submit_feedback_request,
    submit_question_and_generate_answer_request,
    submitted_question_details_request,
    submitted_questions_request,
)
from fai_backend.qaf.schema import QuestionDetails
from fai_backend.schema import ProjectUser, User
from fai_backend.utils import format_datetime_human_readable
from fai_backend.views import page_template

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
async def llm_raq_question_endpoint(question: str):
    try:
        response = await ask_llm_raq_question(question)
        return {'response': response}
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception))


def two_column_layout(page_title: str, left: list[AnyUI], right: list[AnyUI]) -> list[AnyUI]:
    return page_template(
        c.Div(
            components=[
                c.Div(
                    components=left,
                    class_name='flex-1 overflow-y-scroll'
                ),
                c.Div(components=[
                    c.Div(components=[
                        c.Div(
                            components=right,
                            class_name='card-body'
                        )
                    ], class_name='card sticky top-0')
                ], class_name='flex-1 max-w-md border-l'),
            ],
            class_name='grow flex max-h-[calc(100vh-65px)]'
        ),
        page_title=page_title,
    )


@router.get('/questions/create', response_model=list, response_model_exclude_none=True)
def submit_question_view(
        authenticated_user: User = Depends(get_authenticated_user)
) -> list:
    if len(authenticated_user.projects) == 0:
        return [
            c.Text(
                text=_('no_projects', 'You are not a member of any proj.. wait a mintue, how did you login? 😱'),
                class_name='bg-error text-center font-black text-3xl text-warning h-screen flex  items-center justify-center leading-relaxed',
                element='h1'
            ),
        ]

    return page_template(
        c.Div(components=[
            c.Div(components=[
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
                )
            ], class_name='card-body'),
        ], class_name='card'),
        page_title=_('submit_a_question', 'Create Question'),
    )


@router.post('/questions/create', response_model=list, response_model_exclude_none=True)
def create_question_handler(
        question: QuestionDetails = Depends(submit_question_and_generate_answer_request)
) -> list:
    return page_template(
        c.FireEvent(event=e.GoToEvent(url=f'/questions/{question.id}')),
        page_title=_('submit_a_question', 'Create Question'''),
    )


@router.get('/questions', response_model=list, response_model_exclude_none=True)
def questions_index_view(
        authenticated_user: User | None = Depends(try_get_authenticated_user),
        questions: list[Conversation] = Depends(list_my_questions_request),
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    return page_template(
        c.Div(components=[
            c.Div(components=[
                c.Table(
                    data=[
                        {
                            'subject': question.metadata['subject'],
                            'status': question.status,
                            'link': f'/questions/{question.id}',
                        }
                        for question in questions
                    ],
                    columns=[
                        {'key': 'subject', 'label': 'Subject'},
                        {'key': 'status', 'label': 'Status'},
                        {'key': 'link', 'label': '', 'link_text': 'View'},
                    ],

                    class_name='text-base-content join-item md:table-sm lg:table-md table-auto',
                ),
            ], class_name='overflow-x-auto space-y-4'),
        ], class_name='card bg-base-100 w-full max-w-6xl'),
        page_title=_('my_questions', 'My Questions'),
    )


@router.get('/questions/{conversation_id}', response_model=list, response_model_exclude_none=True)
async def question_details_view(
        authenticated_user: ProjectUser | None = Depends(get_project_user),
        question: QuestionDetails = Depends(my_question_details_request)
) -> list:
    if not question:
        return [c.FireEvent(event=e.GoToEvent(url='/questions'))]
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    def message_factory(message: Message) -> AnyUI:
        return c.Div(components=[
            {
                'user': lambda: c.ChatBubble(content=message.content,
                                             is_self=message.created_by == authenticated_user.email,
                                             user=message.user.capitalize(),
                                             image_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjI1IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXItcm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iOCIgcj0iNSIvPjxwYXRoIGQ9Ik0yMCAyMWE4IDggMCAwIDAtMTYgMCIvPjwvc3ZnPg==',
                                             time=format_datetime_human_readable(message.timestamp.created, 3)),
                'assistant': lambda: c.ChatBubble(content=message.content,
                                                  is_self=False,
                                                  user=message.user.capitalize(),
                                                  image_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjI1IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWJvdCI+PHBhdGggZD0iTTEyIDhWNEg4Ii8+PHJlY3Qgd2lkdGg9IjE2IiBoZWlnaHQ9IjEyIiB4PSI0IiB5PSI4IiByeD0iMiIvPjxwYXRoIGQ9Ik0yIDE0aDIiLz48cGF0aCBkPSJNMjAgMTRoMiIvPjxwYXRoIGQ9Ik0xNSAxM3YyIi8+PHBhdGggZD0iTTkgMTN2MiIvPjwvc3ZnPg==',
                                                  time=format_datetime_human_readable(
                                                      message.timestamp.created, 3)

                                                  ),
            }[message.user if message.user == 'assistant' else 'user']()
        ])

    return two_column_layout(
        page_title='Conversation: ' + str(question.subject),
        left=[message_factory(question.question), *([message_factory(question.answer)] if question.answer else []), ],
        right=[],
    )


@router.get('/reviews', response_model=list, response_model_exclude_none=True)
def reviews_index_view(
        authenticated_user: User | None = Depends(try_get_authenticated_user),
        questions: list[QuestionDetails] = Depends(submitted_questions_request),
) -> list:
    if not authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/login'))]

    return page_template(
        c.Div(components=[
            c.Div(components=[
                c.Table(
                    data=[
                        {
                            'subject': question.subject,
                            'link': f'/reviews/{question.id}',
                        }
                        for question in questions
                    ],
                    columns=[
                        {'key': 'subject', 'label': 'Subject'},
                        {'key': 'link', 'label': '', 'link_text': 'View'},
                    ],

                    class_name='text-base-content join-item md:table-sm lg:table-md table-auto',
                ),
            ], class_name='overflow-x-auto space-y-4'),
        ], class_name='card bg-base-100 w-full max-w-6xl'),
        page_title=_('Inbox', 'Inbox'),
    )


@router.get('/reviews/{conversation_id}', response_model=list, response_model_exclude_none=True)
async def review_details_view(
        authenticated_user: ProjectUser | None = Depends(get_project_user),
        question: QuestionDetails = Depends(submitted_question_details_request),
) -> list:
    if not question:
        return [c.FireEvent(event=e.GoToEvent(url='/questions'))]

    def message_factory(message: Message) -> AnyUI:
        return {
            'user': lambda: c.ChatBubble(content=message.content,
                                         is_self=message.created_by == authenticated_user.email,
                                         user=message.user.capitalize(),
                                         image_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjI1IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXItcm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iOCIgcj0iNSIvPjxwYXRoIGQ9Ik0yMCAyMWE4IDggMCAwIDAtMTYgMCIvPjwvc3ZnPg==',
                                         time=format_datetime_human_readable(message.timestamp.created, 3)),
            'assistant': lambda: c.ChatBubble(content=message.content,
                                              is_self=message.created_by == authenticated_user.email,
                                              user=message.user.capitalize(),
                                              image_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjI1IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXItcm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iOCIgcj0iNSIvPjxwYXRoIGQ9Ik0yMCAyMWE4IDggMCAwIDAtMTYgMCIvPjwvc3ZnPg==',
                                              time=format_datetime_human_readable(message.timestamp.created, 3)),
        }[message.user if message.user == 'assistant' else 'user']()

    components = [
        *[message_factory(message) for message in question.messages],
    ]

    render_form = ({
        'feedback_form': lambda: [
            c.Form(
                submit_url=f'/api/reviews/{question.id}/feedback',
                method='POST',
                submit_text=_('create_question_submit_button', 'Submit'),
                components=[
                    c.Text(text=_('review_answer', 'Review answer'), element='h2', class_name='text-lg'),
                    c.InputField(html_type='hidden', name='question_id', value=question.id, hidden=True),
                    c.Select(
                        name='rating',
                        title=_('rating', 'Rating'),
                        options=[
                            ('approved', 'Approved'),
                            ('rejected', 'Rejected'),
                        ],
                    ),
                    c.Textarea(
                        name='comment',
                        title=_('comment', 'Comment'),
                        placeholder=_('input_comment_placeholder', 'Enter a comment here'),
                        required=True,
                    ),
                ],
            ),
        ],
        'answer_form': lambda: [
            c.Form(
                submit_url=f'/api/reviews/{question.id}/answer',
                method='POST',
                submit_text=_('create_question_submit_button', 'Submit'),
                components=[
                    c.Text(text=_('answer', 'Answer')),
                    c.InputField(html_type='hidden', name='question_id', value=question.id, hidden=True),
                    c.Textarea(
                        name='answer',
                        title=_('answer', 'Answer'),
                        placeholder=_('input_comment_placeholder', 'Enter correct answer'),
                        required=True,
                    ),
                ],
            )
        ],
        'null': lambda: [],
    }[
        'feedback_form' if question.review_status is None
        else 'answer_form' if question.review_status == 'rejected' and question.answer is None
        else 'null'
    ])

    return two_column_layout(
        page_title='Review: ' + str(question.subject),
        left=components,
        right=[*render_form()],
    )


@router.post('/reviews/{conversation_id}/feedback', response_model=list, response_model_exclude_none=True)
def submit_feedback_handler(
        conversation_id: str,
        review: QuestionDetails = Depends(submit_feedback_request)
) -> list:
    return page_template(
        c.FireEvent(event=e.GoToEvent(url=f'/reviews/{review.id}')),
        page_title=_('submit_a_question', 'Create Question'''),
    )


@router.post('/reviews/{conversation_id}/answer', response_model=list, response_model_exclude_none=True)
def submit_answer_handler(
        conversation_id: str,
        review: QuestionDetails = Depends(submit_answer_request)
) -> list:
    return page_template(
        c.FireEvent(event=e.GoToEvent(url=f'/reviews/{review.id}')),
        page_title=_('submit_a_question', 'Create Question'''),
    )
