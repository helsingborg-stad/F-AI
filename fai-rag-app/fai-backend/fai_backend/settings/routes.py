from fastapi import APIRouter, Security, Depends
from pydantic import BaseModel, SecretStr

from fai_backend.auth.security import check_permissions
from fai_backend.dependencies import get_authenticated_user, get_project_user_permissions, \
    get_page_template_for_logged_in_users
from fai_backend.framework import components as c
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.settings.models import SettingsDict
from fai_backend.settings.service import SettingsServiceFactory

router = APIRouter(
    prefix='/api',
    tags=['Settings'],
    route_class=LoggingAPIRouter,
    dependencies=[]
)


class GetSettingsResponseModel(BaseModel):
    settings: SettingsDict


@router.get(
    '/settings',
    response_model=GetSettingsResponseModel,
    dependencies=[Security(get_authenticated_user)]
)
async def get_settings(
        permissions=Depends(get_project_user_permissions)
):
    check_permissions(['can_edit_settings'], permissions)
    service = SettingsServiceFactory().get_service()
    settings = (await service.get_all()).model_dump()
    for key in settings.keys():
        if isinstance(settings[key], SecretStr):
            secret: SecretStr = settings[key]
            settings[key] = secret.get_secret_value()
    return GetSettingsResponseModel(settings=settings)


class SetSettingsRequestModel(BaseModel):
    settings: SettingsDict


@router.post(
    '/settings',
    dependencies=[Security(get_authenticated_user)]
)
async def set_settings(
        body: SetSettingsRequestModel,
        permissions=Depends(get_project_user_permissions)
):
    check_permissions(['can_edit_settings'], permissions)
    service = SettingsServiceFactory.get_service()
    await service.set_all(body.settings)


@router.post(
    '/settings/form',
    response_model=list,
    response_model_exclude_none=True
)
async def set_settings_from_form(
        _=Depends(set_settings),
        view=Depends(get_page_template_for_logged_in_users)
):
    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Text(text='Settings updated!'),
            ], class_name='card-body'),
        ], class_name='card')],
        'Edit settings',
    )


@router.get(
    '/view/settings',
    dependencies=[Security(get_authenticated_user)],
    response_model=list,
    response_model_exclude_none=True
)
async def edit_settings(
        permissions=Depends(get_project_user_permissions),
        view=Depends(get_page_template_for_logged_in_users),
):
    check_permissions(['can_edit_settings'], permissions)
    settings = await SettingsServiceFactory.get_service().get_all()

    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Form(
                    submit_url='/api/settings/form',
                    method='POST',
                    submit_text=_('edit_settings_submit_button', 'Submit'),
                    components=[
                        c.Heading(text='Basic', class_name='font-bold'),
                        c.InputField(
                            name='settings.FIXED_PIN',
                            label=_('Fixed login pin (leave blank to disable)'),
                            placeholder='NOTE: Make sure Brevo API is setup correctly to avoid account lock-out!',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.FIXED_PIN,
                        ),

                        c.Heading(text='AI Settings', class_name='font-bold'),
                        c.InputField(
                            name='settings.OPENAI_API_KEY',
                            label=_('OpenAI API Key'),
                            placeholder='sk-proj-...',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.OPENAI_API_KEY.get_secret_value(),
                        ),
                        c.InputField(
                            name='settings.HF_TOKEN',
                            label=_('HuggingFace API Token (optional, for counting vLLM tokens)'),
                            placeholder='hf_...',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.HF_TOKEN.get_secret_value(),
                        ),
                        c.Textarea(
                            name='settings.VLLM_CONFIG',
                            label=_('vLLM Config (optional, for non-OpenAI models)'),
                            placeholder='',
                            required=False,
                            size='sm',
                            value=settings.VLLM_CONFIG,
                        ),
                        c.Select(
                            name='settings.APP_VECTOR_DB_EMBEDDING_MODEL',
                            label=_('Embedding model'),
                            required=True,
                            size='sm',
                            options=[
                                ('default', 'default'),
                                ('text-embedding-3-small', 'text-embedding-3-small')
                            ],
                            value=settings.APP_VECTOR_DB_EMBEDDING_MODEL,
                        ),

                        c.Heading(text='E-mail (Brevo)', class_name='font-bold'),
                        c.InputField(
                            name='settings.BREVO_API_URL',
                            label=_('Brevo API URL'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.BREVO_API_URL,
                        ),
                        c.InputField(
                            name='settings.BREVO_API_KEY',
                            label=_('Brevo API Key'),
                            placeholder='xkeysib-...',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.BREVO_API_KEY.get_secret_value(),
                        ),
                        c.InputField(
                            name='settings.MAIL_SENDER_NAME',
                            label=_('Sender name'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.MAIL_SENDER_NAME,
                        ),
                        c.InputField(
                            name='settings.MAIL_SENDER_EMAIL',
                            label=_('Sender email'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.MAIL_SENDER_EMAIL,
                        ),

                        c.Heading(text='Analytics (Sentry) (changes requires server restart)', class_name='font-bold'),
                        c.InputField(
                            name='settings.SENTRY_DSN',
                            label=_('DSN'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.SENTRY_DSN.get_secret_value(),
                        ),
                        c.InputField(
                            name='settings.SENTRY_ENVIRONMENT',
                            label=_('Environment'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.SENTRY_ENVIRONMENT,
                        ),
                        c.Range(
                            name='settings.SENTRY_TRACE_SAMPLE_RATE',
                            label=_('Trace sample rate'),
                            required=True,
                            size='sm',
                            min=0.0,
                            max=1.0,
                            step=0.05,
                            value=settings.SENTRY_TRACE_SAMPLE_RATE,
                        ),
                        c.Select(
                            name='settings.SENTRY_LOGGING_LEVEL',
                            label=_('Logging level'),
                            required=True,
                            size='sm',
                            options=[
                                ('CRITICAL', 'CRITICAL'),
                                ('FATAL', 'FATAL'),
                                ('ERROR', 'ERROR'),
                                ('WARN', 'WARN'),
                                ('WARNING', 'WARNING'),
                                ('INFO', 'INFO'),
                                ('DEBUG', 'DEBUG'),
                            ],
                            value=settings.SENTRY_LOGGING_LEVEL,
                        ),
                        c.Select(
                            name='settings.SENTRY_EVENT_LEVEL',
                            label=_('Logging level'),
                            required=True,
                            size='sm',
                            options=[
                                ('CRITICAL', 'CRITICAL'),
                                ('FATAL', 'FATAL'),
                                ('ERROR', 'ERROR'),
                                ('WARN', 'WARN'),
                                ('WARNING', 'WARNING'),
                                ('INFO', 'INFO'),
                                ('DEBUG', 'DEBUG'),
                            ],
                            value=settings.SENTRY_EVENT_LEVEL,
                        ),

                        c.Heading(text='Feedback', class_name='font-bold'),
                        c.InputField(
                            name='settings.FEEDBACK_GITHUB_API_TOKEN',
                            label=_('GitHub API token'),
                            placeholder='ghp_...',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.FEEDBACK_GITHUB_API_TOKEN.get_secret_value(),
                        ),
                        c.InputField(
                            name='settings.FEEDBACK_GITHUB_REPO_OWNER',
                            label=_('GitHub repo owner'),
                            placeholder='helsingborg-stad',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.FEEDBACK_GITHUB_REPO_OWNER,
                        ),
                        c.InputField(
                            name='settings.FEEDBACK_GITHUB_REPO_NAME',
                            label=_('GitHub repo name'),
                            placeholder='F-AI',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings.FEEDBACK_GITHUB_REPO_NAME,
                        ),
                    ]
                )
            ], class_name='card-body')
        ], class_name='card')
        ],
        _('Edit settings')
    )
