from fastapi import APIRouter, Security, Depends

from fai_backend.auth.security import check_permissions
from fai_backend.config import get_settings_dict
from fai_backend.config_v2.models import Config
from fai_backend.dependencies import get_authenticated_user, get_project_user_permissions, get_project_user, \
    get_page_template_for_logged_in_users
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.projects.dependencies import get_project_service
from fai_backend.projects.service import ProjectService
from fai_backend.schema import ProjectUser
from fai_backend.framework import components as c
from fai_backend.phrase import phrase as _
from fastapi import APIRouter, Security, Depends

from fai_backend.auth.security import check_permissions
from fai_backend.config import get_settings_dict
from fai_backend.config_v2.models import Config
from fai_backend.dependencies import get_authenticated_user, get_project_user_permissions, get_project_user, \
    get_page_template_for_logged_in_users
from fai_backend.framework import components as c
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import get_project_service
from fai_backend.projects.service import ProjectService
from fai_backend.schema import ProjectUser

router = APIRouter(
    prefix='/api',
    tags=['Config'],
    route_class=LoggingAPIRouter,
    dependencies=[]
)

GetConfigResponseModel = Config


@router.get(
    '/config',
    response_model=GetConfigResponseModel,
    dependencies=[Security(get_authenticated_user)]
)
async def get_config(
        permissions=Depends(get_project_user_permissions),
        project_user: ProjectUser = Depends(get_project_user),
        project_service: ProjectService = Depends(get_project_service)
):
    check_permissions(['can_edit_config'], permissions)
    project = await project_service.read_project(project_user.project_id)
    settings = get_settings_dict(project.config.config)
    return GetConfigResponseModel(config=settings)


@router.post(
    '/config',
    dependencies=[Security(get_authenticated_user)]
)
async def set_config(
        body: Config,
        permissions=Depends(get_project_user_permissions),
        project_user: ProjectUser = Depends(get_project_user),
        project_service: ProjectService = Depends(get_project_service)
):
    check_permissions(['can_edit_config'], permissions)
    project = await project_service.read_project(project_user.project_id)
    project.config = body
    await project_service.update_project(project_user.project_id, project)


@router.post(
    '/config/form'
)
async def set_config_from_form(
        _=Depends(set_config),
        view=Depends(get_page_template_for_logged_in_users),
):
    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Text(text='bla'),
            ], class_name='card-body'),
        ], class_name='card')],
        'bla',
    )


@router.get(
    '/view/config',
    dependencies=[Security(get_authenticated_user)],
    response_model=list,
    response_model_exclude_none=True
)
async def edit_config(
        permissions=Depends(get_project_user_permissions),
        project_user: ProjectUser = Depends(get_project_user),
        project_service: ProjectService = Depends(get_project_service),
        view=Depends(get_page_template_for_logged_in_users),
):
    check_permissions(['can_edit_config'], permissions)
    project = await project_service.read_project(project_user.project_id)
    full_config = get_settings_dict(project.config.config)

    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Form(
                    submit_url='/api/config/form',
                    method='POST',
                    submit_text=_('edit_config_submit_button', 'Submit'),
                    components=[
                        c.Heading(text='Basic', class_name='font-bold'),
                        c.InputField(
                            name='config.FIXED_PIN',
                            label=_('Fixed pin (leave blank to disable)'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=str(full_config.get('FIXED_PIN', '')),
                        ),

                        c.Heading(text='AI Settings', class_name='font-bold'),
                        c.InputField(
                            name='config.OPENAI_API_KEY',
                            label=_('OpenAI API Key'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=full_config.get('OPENAI_API_KEY', ''),
                        ),
                        c.Textarea(
                            name='config.VLLM_CONFIG',
                            label=_('VLLM Config'),
                            placeholder='',
                            required=False,
                            size='sm',
                            value=full_config.get('VLLM_CONFIG', ''),
                        ),

                        c.Heading(text='E-mail (Brevo)', class_name='font-bold'),
                        c.InputField(
                            name='config.BREVO_API_URL',
                            label=_('Brevo API URL'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=full_config.get('BREVO_API_URL', ''),
                        ),
                        c.InputField(
                            name='config.BREVO_API_KEY',
                            label=_('Brevo API Key'),
                            placeholder=_(''),
                            required=False,
                            html_type='text',
                            size='sm',
                            value=full_config.get('BREVO_API_KEY', ''),
                        )
                    ]
                )
            ], class_name='card-body')
        ], class_name='card')
        ],
        _('Edit config')
    )
