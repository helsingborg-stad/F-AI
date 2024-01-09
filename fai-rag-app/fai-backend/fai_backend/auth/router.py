from fastapi import APIRouter, Depends
from fastui import AnyComponent, FastUI

from fai_backend.auth.views import login_handler, login_page, logout_handler, verify_handler
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter

router = APIRouter(
    prefix='/api',
    tags=['Auth'],
    route_class=LoggingAPIRouter,
)


@router.get('/login', response_model=FastUI, response_model_exclude_none=True)
def login_view(
        view: list[AnyComponent] = Depends(login_page),
) -> list[AnyComponent]:
    return view


@router.get('/logout', response_model=FastUI, response_model_exclude_none=True)
def logout(
        on_logout: list[AnyComponent] = Depends(logout_handler),
) -> list[AnyComponent]:
    return on_logout


@router.post('/login', response_model=FastUI, response_model_exclude_none=True)
def login(
        on_login: list[AnyComponent] = Depends(login_handler),
) -> list[AnyComponent]:
    return on_login


@router.post('/login/verify', response_model=FastUI, response_model_exclude_none=True)
def verify(
        on_verify: list[AnyComponent] = Depends(verify_handler),
) -> list[AnyComponent]:
    return on_verify
