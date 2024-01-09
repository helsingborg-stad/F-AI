from typing import Annotated

from fastapi import Depends, Form, HTTPException, Response, Security
from fastapi_jwt import JwtAuthorizationCredentials
from pydantic import EmailStr, SecretStr

from fai_backend.auth.schema import (
    RequestPin,
    RequestPinVerification,
    ResponsePin,
    ResponseToken,
    TokenPayload,
)
from fai_backend.auth.security import (
    access_security,
    api_key_header,
    refresh_security,
)
from fai_backend.auth.service import AuthService
from fai_backend.repositories import pins_repo, users_repo

api_keys = ['test']


async def get_auth_service() -> AuthService:
    return AuthService(users_repo=users_repo, pins_repo=pins_repo)


def try_get_valid_api_key(api_key: str = Security(api_key_header)) -> str | None:
    return api_key if api_key in api_keys else None


async def try_get_valid_access_token(
        credentials: JwtAuthorizationCredentials | None = Security(access_security),
) -> JwtAuthorizationCredentials | None:
    return credentials


async def try_get_valid_refresh_token(
        credentials: JwtAuthorizationCredentials = Security(refresh_security),
) -> EmailStr:
    return credentials.subject['email']


def try_get_access_token_payload(
        credentials: JwtAuthorizationCredentials | None = Security(
            try_get_valid_access_token
        ),
) -> TokenPayload | None:
    if credentials:
        return TokenPayload.model_validate(credentials.subject)
    return None


def try_get_refresh_token_payload(
        credentials: JwtAuthorizationCredentials | None = Security(
            try_get_valid_access_token
        ),
) -> TokenPayload | None:
    if credentials:
        return TokenPayload.model_validate(credentials.subject)
    return None


async def valid_user_email(
        body: RequestPin | None = None,
        email: Annotated[EmailStr | None, Form()] = None,
        auth_service: AuthService = Depends(get_auth_service),
) -> EmailStr:
    email = body.email if body else email
    if await auth_service.email_exists(email):
        return email
    else:
        raise HTTPException(status_code=404, detail='User not found')


async def valid_session_id(
        session_id: str | None = None,
        auth_service: AuthService = Depends(get_auth_service),
) -> str | None:
    if session_id:
        if await auth_service.session_exists(session_id):
            return session_id
        return ''

    return None


async def make_temporary_pin(
        email: EmailStr = Depends(valid_user_email),
        auth_service: AuthService = Depends(get_auth_service),
) -> ResponsePin:
    session_id = await auth_service.create_pin(email)
    return ResponsePin(email=email, session_id=session_id)


async def try_exchange_pin_for_token(
        response: Response,
        session_id: Annotated[str | None, Form()] = '',
        pin: Annotated[SecretStr | None, Form()] = '',
        body: RequestPinVerification | None = None,
        auth_service: AuthService = Depends(get_auth_service),
) -> ResponseToken:
    session_id = body.session_id if body else session_id
    pin = body.pin if body else pin
    try:
        return await auth_service.exchange_pin_for_token(session_id, pin, response)
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid credentials')


async def make_refresh_token(
        response: Response,
        email: EmailStr = Security(try_get_valid_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
) -> ResponseToken:
    return await auth_service.refresh_token(email, response)
