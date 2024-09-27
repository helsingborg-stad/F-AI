from fai_backend.assistant.schema import TemplatePayload
from fai_backend.framework import components as c
from fai_backend.phrase import phrase as _


def AssistantForm(
        submit_url: str,
        data: TemplatePayload | None = None,
        collection_ids: list[str] | None = None,
) -> list:
    return [c.Div(components=[
        c.Div(components=[

            c.Form(
                id=f'assistant-form-{data.id}' if data else 'assistant-form',
                submit_url=submit_url,
                method='POST',
                submit_text=_('create_question_submit_button', 'Submit'),
                components=[

                    c.InputField(
                        name='name',
                        label=_('Name'),
                        placeholder=_('Name'),
                        required=True,
                        html_type='text',
                        size='sm',
                        value=data.name if data else '',
                    ),

                    c.Textarea(
                        name='instructions',
                        label=_('Instructions'),
                        placeholder=_('Enter instructions here'),
                        required=True,
                        size='sm',
                        value=data.instructions if data else '',
                    ),

                    c.Select(
                        name='model',
                        label=_('input_label_model', 'Model'),
                        placeholder=_('input_model_placeholder', 'Select model'),
                        required=True,
                        options=[
                            ('gpt-3.5-turbo', _('GPT-3.5 Turbo')),
                            ('gpt-4o', _('GPT-4o')),
                            ('gpt-4', _('GPT-4')),
                        ],
                        value=data.model if data else 'gpt-3.5-turbo',
                        size='sm',
                    ),

                    c.Range(
                        name='temperature',
                        label=_('input_temperature_label', 'Temperature'),
                        required=True,
                        value=data.temperature if data else 1.0,
                        size='sm',
                        min=0.01,
                        max=2.00,
                        step=0.01,
                    ),

                    c.Select(
                        name='files_collection_id',
                        label=_('Collection ID'),
                        required=False,
                        options=[
                            ('', _('None')),
                            *([(cid, cid) for cid in collection_ids] if collection_ids else []),
                        ],
                        value=data.files_collection_id if data and data.files_collection_id else '',
                        size='sm',
                    ),

                    c.Textarea(
                        name='description',
                        label=_('Description (optional)'),
                        placeholder=_('This is a description that will be shown when starting a new chat'),
                        required=False,
                        size='sm',
                        value=data.description if data and data.description else '',
                    ),
                    c.InputField(
                        name='sample_questions[0]',
                        label=_('Example question 1 (optional)'),
                        placeholder=_('What is the capital of Sweden?'),
                        required=False,
                        html_type='text',
                        size='sm',
                        value=data.sample_questions[0] if data and data.sample_questions and len(
                            data.sample_questions) > 0 else '',
                    ),

                    c.InputField(
                        name='sample_questions[1]',
                        label=_('Example question 2 (optional)'),
                        placeholder=_('What is the capital of Norway?'),
                        required=False,
                        html_type='text',
                        size='sm',
                        value=data.sample_questions[1] if data and data.sample_questions and len(
                            data.sample_questions) > 1 else '',
                    ),

                    c.InputField(
                        name='sample_questions[2]',
                        label=_('Example question 3 (optional)'),
                        placeholder=_('What is the capital of Denmark?'),
                        required=False,
                        html_type='text',
                        size='sm',
                        value=data.sample_questions[2] if data and data.sample_questions and len(
                            data.sample_questions) > 2 else '',
                    ),
                ],
            )
        ], class_name='card-body'),
    ], class_name='card')]
