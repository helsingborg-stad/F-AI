from fastapi import APIRouter, Security, Depends
from pydantic import BaseModel

from fai_backend.auth.security import check_permissions
from fai_backend.dependencies import (get_authenticated_user, get_project_user_permissions,
                                      get_page_template_for_logged_in_users)
from fai_backend.framework import components as c
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import get_project_service
from fai_backend.settings.models import SettingsDict
from fai_backend.settings.service import SettingsServiceFactory
from fai_backend.config import settings as app_settings

router = APIRouter(
    prefix='/api',
    tags=['Settings'],
    route_class=LoggingAPIRouter,
    dependencies=[]
)


class GetSettingsResponseModel(BaseModel):
    settings: SettingsDict


class SetSettingsRequestModel(BaseModel):
    settings: SettingsDict


@router.get(
    '/settings',
    response_model=GetSettingsResponseModel,
    dependencies=[Security(get_authenticated_user)])
async def get_settings(
        permissions=Depends(get_project_user_permissions),
        project_service=Depends(get_project_service)):
    check_permissions(['can_edit_settings'], permissions)
    service = SettingsServiceFactory().get_service(project_service)
    settings = (await service.get_all(app_settings)).model_dump()
    return GetSettingsResponseModel(settings=settings)


@router.post(
    '/settings',
    dependencies=[Security(get_authenticated_user)])
async def set_settings(
        body: SetSettingsRequestModel,
        permissions=Depends(get_project_user_permissions),
        project_service=Depends(get_project_service)):
    check_permissions(['can_edit_settings'], permissions)
    service = SettingsServiceFactory.get_service(project_service)
    await service.set_all(body.settings, app_settings)


@router.post(
    '/settings/form',
    response_model=list,
    response_model_exclude_none=True)
async def set_settings_from_form(
        _=Depends(set_settings),
        view=Depends(get_page_template_for_logged_in_users)):
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
    response_model_exclude_none=True)
async def edit_settings(
        permissions=Depends(get_project_user_permissions),
        view=Depends(get_page_template_for_logged_in_users),
        project_service=Depends(get_project_service)):
    check_permissions(['can_edit_settings'], permissions)
    settings = await SettingsServiceFactory.get_service(project_service).get_all(app_settings)

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
                            label=_('Fixed pin (leave blank to disable)'),
                            placeholder='NOTE: Make sure Brevo API is setup correctly to avoid account lock-out!',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings['FIXED_PIN'] or None,
                        ),

                        c.Heading(text='AI Settings', class_name='font-bold'),
                        c.InputField(
                            name='settings.OPENAI_API_KEY',
                            label=_('OpenAI API Key'),
                            placeholder='sk-proj-...',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings['OPENAI_API_KEY'] or None,
                        ),

                        c.Heading(text='E-mail (Brevo)', class_name='font-bold'),
                        c.InputField(
                            name='settings.BREVO_API_URL',
                            label=_('Brevo API URL'),
                            placeholder='',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings['BREVO_API_URL'] or None,
                        ),
                        c.InputField(
                            name='settings.BREVO_API_KEY',
                            label=_('Brevo API Key'),
                            placeholder='xkeysib-...',
                            required=False,
                            html_type='text',
                            size='sm',
                            value=settings['BREVO_API_KEY'] or None,
                        )
                    ]
                )
            ], class_name='card-body')
        ], class_name='card')
        ],
        _('Edit settings')
    )
