from typing import Optional

from fastapi import Depends, Response
from fastui import AnyComponent, components as c
from fastui.events import GoToEvent, AuthEvent

from fai_backend.auth.dependencies import (
    valid_session_id,
    make_temporary_pin,
    try_exchange_pin_for_token,
)
from fai_backend.auth.schema import RequestPin, ResponsePin, ResponseToken
from fai_backend.auth.security import access_security, refresh_security
from fai_backend.dependencies import try_get_authenticated_user
from fai_backend.schema import User


def login_form() -> list[AnyComponent]:
    return [
        c.Div(
            components=[
                c.Heading(text="Login"),
            ],
            class_name="text-center",
        ),
        c.ModelForm(
            model=RequestPin,
            submit_url="/api/login",
            class_name="col-xs-12",
            footer=[c.Button(text="Login", html_type="submit")],
        ),
    ]


def login_handler(
    session_info: ResponsePin = Depends(make_temporary_pin),
) -> list[AnyComponent]:
    return [
        c.FireEvent(
            event=GoToEvent(url="/login", query={"session_id": session_info.session_id})
        )
    ]


def verify_form(session_id: str) -> list[AnyComponent]:
    return [
        c.Div(
            components=[
                c.Heading(text="Login"),
            ],
            class_name="text-center",
        ),
        c.Form(
            submit_url="/api/login/verify",
            form_fields=[
                c.FormFieldInput(
                    name="session_id",
                    title="",
                    html_type="hidden",
                    initial=session_id,
                    hidden=True,
                ),
                c.FormFieldInput(
                    name="pin",
                    title="PIN",
                    required=True,
                    html_type="password",
                ),
            ],
            method="POST",
            class_name="col-xs-12",
        ),
    ]


def verify_handler(
    token: ResponseToken = Depends(try_exchange_pin_for_token),
) -> list[AnyComponent]:
    return [c.FireEvent(event=AuthEvent(token=token.access_token, url="/"))]


def login_page(
    session_id: Optional[str] = Depends(valid_session_id),
    user: Optional[User] = Depends(try_get_authenticated_user),
) -> list[AnyComponent]:
    if user:
        return [c.FireEvent(event=GoToEvent(url="/"))]

    if session_id == "":
        return [c.FireEvent(event=GoToEvent(url="/login", query={"session_id": None}))]

    form = (lambda: verify_form(session_id)) if session_id is not None else login_form

    return [
        c.Page(
            components=[
                c.Div(
                    components=[c.Div(components=form(), class_name="col-md-4")],
                    class_name="row justify-content-center",
                )
            ]
        )
    ]


def logout_handler(
    response: Response,
    user: Optional[User] = Depends(try_get_authenticated_user),
) -> list[AnyComponent]:
    if not user:
        return [c.FireEvent(event=GoToEvent(url="/login"))]
    access_security.unset_access_cookie(response)
    refresh_security.unset_refresh_cookie(response)
    return [c.FireEvent(event=AuthEvent(token=False, url="/login"))]
