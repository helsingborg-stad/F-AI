from fastapi import APIRouter, Depends, Response

from fai_backend.auth.dependencies import (
    make_temporary_pin,
    try_exchange_pin_for_token,
    valid_session_id,
)
from fai_backend.auth.schema import ResponsePin, ResponseToken
from fai_backend.auth.security import access_security, refresh_security
from fai_backend.dependencies import try_get_authenticated_user
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.schema import User

router = APIRouter(
    prefix='/api',
    tags=['Auth'],
    route_class=LoggingAPIRouter,
)


@router.get('/login', response_model=list, response_model_exclude_none=True)
def login_view(
        session_id: str | None = Depends(valid_session_id),
        authenticated_user: User | None = Depends(try_get_authenticated_user),
) -> list:
    if authenticated_user:
        return [c.FireEvent(event=e.GoToEvent(url='/'))]

    if session_id == '':
        return [c.FireEvent(event=e.GoToEvent(url='/login', query={'session_id': None}))]

    render_form = ({
        'request_pin': lambda: [
            c.Form(
                submit_url='/api/login',
                method='POST',
                components=[
                    c.InputField(
                        name='email',
                        title=_('input_email_label', 'Email'),
                        placeholder=_('input_email_placeholder', 'Enter email'),
                        required=True,
                        html_type='email',
                    ),
                    c.Button(
                        state='neutral',
                        label=_('request_pin_submit_button', 'Send One-time PIN'),
                        html_type='submit',
                        block=True,
                    )
                ]
            ),
        ],
        'verify_pin': lambda: [
            c.Form(
                submit_url='/api/login/verify',
                method='POST',
                components=[
                    c.InputField(
                        name='pin',
                        title=_('input_pin_label', 'PIN'),
                        placeholder=_('input_pin_placeholder', 'Enter One-time PIN'),
                        required=True,
                        html_type='password',
                        autocomplete='one-time-code',
                    ),
                    c.InputField(
                        name='session_id',
                        title='',
                        html_type='hidden',
                        initial=session_id,
                        required=True,
                        hidden=True,
                        readonly=True,
                    ),
                    c.Button(
                        state='neutral',
                        label=_('verify_pin_submit_button', 'Authenticate'),
                        html_type='submit',
                        block=True,
                    )
                ],
            ),
        ]
    }['verify_pin' if session_id is not None else 'request_pin'])

    return [
        c.Div(
            components=[
                c.Div(
                    components=[
                        c.Div(
                            components=[
                                c.Heading(
                                    text='PIN' if session_id is not None else 'Login',
                                    class_name='text-4xl font-extrabold text-center mb-6 mt-0',
                                ),
                                *render_form(),
                            ],
                            class_name='card-body',
                        )
                    ],
                    class_name='card bg-base-200 w-full max-w-sm mx-auto pt-6',
                )
            ],
            class_name='h-screen flex justify-center items-center',
        )
    ]


@router.post('/login', response_model=list, response_model_exclude_none=True)
def request_pin_handler(
        session_info: ResponsePin = Depends(make_temporary_pin),
) -> list:
    return [c.FireEvent(event=e.GoToEvent(url='/login', query={'session_id': session_info.session_id}))]


@router.post('/login/verify', response_model=list, response_model_exclude_none=True)
async def verify_pin_handler(
        token: ResponseToken = Depends(try_exchange_pin_for_token),
) -> list:
    return [c.FireEvent(event=e.GoToEvent(url='/'))]


@router.get('/logout', response_model=list, response_model_exclude_none=True)
def logout_handler(
        response: Response,
        user: User | None = Depends(try_get_authenticated_user),
) -> list:
    if user:
        access_security.unset_access_cookie(response)
        refresh_security.unset_refresh_cookie(response)
    return [c.FireEvent(event=e.GoToEvent(url='/login'))]
