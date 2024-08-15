from urllib.parse import urlencode

from fai_backend.conversations.schema import ResponseMessage
from fai_backend.framework import components as c
from fai_backend.framework.components import AnyUI
from fai_backend.phrase import phrase as _
from fai_backend.qaf.schema import QuestionDetails
from fai_backend.schema import ProjectUser
from fai_backend.utils import format_datetime_human_readable


def message_factory(authenticated_user, message: ResponseMessage) -> AnyUI:
    return {
        'user': lambda: c.ChatBubble(content=message.content,
                                     is_self=True,
                                     user=message.user.capitalize(),
                                     image_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjI1IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXItcm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iOCIgcj0iNSIvPjxwYXRoIGQ9Ik0yMCAyMWE4IDggMCAwIDAtMTYgMCIvPjwvc3ZnPg==',
                                     time=format_datetime_human_readable(message.timestamp.created, 3)),
        'assistant': lambda: c.ChatBubble(content=message.content,
                                          is_self=False,
                                          user=message.user.capitalize(),
                                          image_src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0OCIgaGVpZ2h0PSI0OCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjI1IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLXVzZXItcm91bmQiPjxjaXJjbGUgY3g9IjEyIiBjeT0iOCIgcj0iNSIvPjxwYXRoIGQ9Ik0yMCAyMWE4IDggMCAwIDAtMTYgMCIvPjwvc3ZnPg==',
                                          time=format_datetime_human_readable(message.timestamp.created, 3)),
    }[message.user if message.user == 'assistant' else 'user']()


def two_column_layout(left: list[any], right: list[any]) -> list[any]:
    return [
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
        )
    ]


def QuestionsDataTable(
        data: list,
        columns: list[dict],
        query_params: dict,
        view
):
    def map_sort_query_onto_columns(
            column_data: list[dict],
            filter_params: dict | None,
            sortable_keys: list[str] | None,
            default_sort_key: str | None,
            default_order: str | None
    ) -> list[dict]:
        current_key = filter_params['sort'] \
            if filter_params and filter_params['sort'] in sortable_keys \
            else default_sort_key

        current_order = filter_params['sort_order'] \
            if (filter_params
                and filter_params['sort_order']
                and filter_params['sort_order'] in ['asc', 'desc']) \
            else default_order

        reverse_order = 'asc' if current_order == 'desc' else 'desc'

        if not current_key:
            return column_data

        return list(map(
            lambda col: {
                **col,
                'sortable': col['key'] in [*(sortable_keys or []), *(default_sort_key or [])],
                'sort_order': current_order if col['key'] == current_key else None,
                'sort_url': '?' + urlencode({**filter_params, 'sort': col['key'],
                                             'sort_order': reverse_order if col['key'] == current_key else 'desc'}),
            },
            column_data
        ))

    table = c.Table(
        data=data,
        columns=map_sort_query_onto_columns(
            columns,
            query_params,
            ['timestamp.modified', 'timestamp.created'],
            'timestamp.modified',
            'desc'
        ),

        class_name='text-base-content join-item md:table-sm lg:table-md table-auto',
    )

    return view(
        [c.Div(components=[
            c.Div(components=[
                # c.CustomComponent(component='async'),
                table
            ], class_name='overflow-x-auto space-y-4'),
        ], class_name='card bg-base-100 w-full max-w-6xl')],
        _('Inbox', 'Inbox'),
    )


def QuestionsMeta(
        data: dict,
        fields: list[dict],
):
    return c.Table(
        data=[
            {
                'label': field['label'] if 'label' in field else field['key'],
                'value': data[field['key']] if field['key'] in data else 'None'
            }
            for field in fields
        ],
        columns=[
            {
                'key': 'label',
                'label': 'Field',
            },
            {
                'key': 'value',
                'label': 'Value',
            },
        ],
        class_name='text-base-content join-item md:table-xs lg:table-sm table-auto',
    )


def QuestionForm(view, submit_url: str):
    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Form(
                    submit_url=submit_url,
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
                        c.Radio(
                            name='tags[0]',
                            title=_('input_quality_tag',
                                    'How is the AI expected to be able to respond to this question?'),
                            required=True,
                            options=[
                                ('quality.good',
                                 _('question_quality_good', '✅ AI is expected to answer the question correctly')),
                                ('quality.ok', _('question_quality_ok', '🟡 AI might not be able to answer')),
                                ('quality.bad', _('question_quality_bad', '❌ AI is not expected to provide an answer')),
                            ],
                        )
                    ],
                )
            ], class_name='card-body'),
        ], class_name='card')],
        _('submit_a_question', 'Create Question'),
    )


def ReviewDetailsMeta(question: QuestionDetails):
    return []


def ReviewDetailsHeader(question: QuestionDetails):
    fields = {
        'type': _('Question'),
        'title': question.question.content
    }

    return [
        c.Div(
            components=[
                c.Text(text=fields['type'], class_name='text-xs'),
                c.Heading(text=fields['title'], level=2, class_name='text-xl')
            ]
        ),
    ]


def ReviewDetails(user: ProjectUser, question: QuestionDetails, view, meta_data: dict = None,
                  meta_fields: list[dict] = None):
    review_state = {
        'open': lambda: [
            c.Form(
                submit_url=f'/api/view/questions/{question.id}/feedback',
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
        'in-progress': lambda: [
            c.Form(
                submit_url=f'/api/view/questions/{question.id}/answer',
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
        'approved': lambda: [],
        'rejected': lambda: [],
        'blocked': lambda: [],
        'null': lambda: [],
    }

    return view(
        two_column_layout(
            left=[message_factory(user, message) for message in question.messages],
            right=[
                *ReviewDetailsHeader(question),
                *review_state[question.review_status](),
                *[QuestionsMeta(
                    data=meta_data,
                    fields=meta_fields
                )],
            ]
        ),
        'Review: ' + str(question.subject)
    )
