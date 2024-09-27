from fai_backend.feedback.providers.protocol import IFeedbackProvider
from fai_backend.framework import components as c
from fai_backend.phrase import phrase as _


def feedback_view(view, submit_url: str) -> list:
    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Form(
                    submit_url=submit_url,
                    method='POST',
                    submit_text=_('create_feedback_submit_button', 'Send'),
                    components=[
                        c.InputField(
                            name='feedback_subject',
                            title=_('input_subject_label', 'Subject'),
                            placeholder=_('input_subject_placeholder', 'Subject'),
                            required=True,
                            html_type='text',
                        ),
                        c.Textarea(
                            name='feedback',
                            title=_('input_label_feedback', 'Feedback'),
                            placeholder=_('input_feedback_placeholder', 'Enter your feedback here'),
                            required=True,
                        ),
                    ],
                )
            ], class_name='card-body'),
        ], class_name='card')],
        _('submit_feedback', 'Send Feedback'),
    )


def feedback_submit_view(view) -> list:
    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Text(text=_('feedback_submitted', 'Feedback received. Thank you! 😊')),
            ], class_name='card-body'),
        ], class_name='card')],
        _('feedback_submitted', 'Send Feedback'),
    )
