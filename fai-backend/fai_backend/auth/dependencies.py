from fastapi import Depends, HTTPException, Response, Security
from fastapi_jwt import JwtAuthorizationCredentials
from pydantic import EmailStr

from fai_backend.auth.schema import (
    RequestPin,
    RequestPinVerification,
    ResponsePin,
    ResponseToken,
    TokenPayload,
)
from fai_backend.auth.security import (
    access_security,
    refresh_security,
)
from fai_backend.auth.service import AuthService
from fai_backend.mail.client import mail_client
from fai_backend.repositories import pins_repo, users_repo


async def get_auth_service() -> AuthService:
    return AuthService(users_repo=users_repo, pins_repo=pins_repo, mail_client=mail_client)


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
        body: RequestPin,
        auth_service: AuthService = Depends(get_auth_service),
) -> EmailStr:
    email_as_lowercase = body.email.lower()

    if await auth_service.email_exists(email_as_lowercase):
        return email_as_lowercase
    else:
        raise HTTPException(status_code=404, detail=[
            {
                'loc': ['body', 'email'],
                'msg': 'User with this email does not exist',
                'type': 'value_error',
            }
        ])


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
        body: RequestPinVerification,
        auth_service: AuthService = Depends(get_auth_service),
) -> ResponseToken:
    try:
        token = await auth_service.exchange_pin_for_token(body.session_id, body.pin, response)
        if not token:
            raise HTTPException(status_code=401, detail='Invalid credentials')
        return token
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid credentials')


async def make_refresh_token(
        response: Response,
        email: EmailStr = Security(try_get_valid_refresh_token),
        auth_service: AuthService = Depends(get_auth_service),
) -> ResponseToken:
    return await auth_service.refresh_token(email, response)
