from typing import Optional, Annotated

from fastapi import Depends, Security, HTTPException, Form, Response
from fastapi_jwt import JwtAuthorizationCredentials
from pydantic import EmailStr, SecretStr

from fai_backend.auth.schema import (
    RequestPin,
    ResponsePin,
    RequestPinVerification,
    ResponseToken,
    TokenPayload,
)
from fai_backend.auth.security import (
    refresh_security,
    api_key_header,
    access_security,
)
from fai_backend.auth.service import AuthService
from fai_backend.repositories import users_repo, pins_repo

api_keys = ["test"]


async def get_auth_service() -> AuthService:
    return AuthService(users_repo=users_repo, pins_repo=pins_repo)


def try_get_valid_api_key(api_key: str = Security(api_key_header)) -> Optional[str]:
    return api_key if api_key in api_keys else None


async def try_get_valid_access_token(
    credentials: Optional[JwtAuthorizationCredentials] = Security(access_security),
) -> Optional[JwtAuthorizationCredentials]:
    return credentials


async def try_get_valid_refresh_token(
    credentials: JwtAuthorizationCredentials = Security(refresh_security),
) -> EmailStr:
    return credentials.subject["email"]


def try_get_access_token_payload(
    credentials: Optional[JwtAuthorizationCredentials] = Security(
        try_get_valid_access_token
    ),
) -> Optional[TokenPayload]:
    if credentials:
        return TokenPayload.model_validate(credentials.subject)
    return None


def try_get_refresh_token_payload(
    credentials: Optional[JwtAuthorizationCredentials] = Security(
        try_get_valid_access_token
    ),
) -> Optional[TokenPayload]:
    if credentials:
        return TokenPayload.model_validate(credentials.subject)
    return None


async def valid_user_email(
    body: Optional[RequestPin] = None,
    email: Annotated[Optional[EmailStr], Form()] = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> EmailStr:
    email = body.email if body else email
    if await auth_service.email_exists(email):
        return email
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def valid_session_id(
    session_id: Optional[str] = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> Optional[str]:
    if session_id:
        if await auth_service.session_exists(session_id):
            return session_id
        return ""

    return None


async def make_temporary_pin(
    email: EmailStr = Depends(valid_user_email),
    auth_service: AuthService = Depends(get_auth_service),
) -> ResponsePin:
    session_id = await auth_service.create_pin(email)
    return ResponsePin(email=email, session_id=session_id)


async def try_exchange_pin_for_token(
    response: Response,
    session_id: Annotated[Optional[str], Form()] = "",
    pin: Annotated[Optional[SecretStr], Form()] = "",
    body: Optional[RequestPinVerification] = None,
    auth_service: AuthService = Depends(get_auth_service),
) -> ResponseToken:
    session_id = body.session_id if body else session_id
    pin = body.pin if body else pin
    try:
        return await auth_service.exchange_pin_for_token(session_id, pin, response)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")


async def make_refresh_token(
    response: Response,
    email: EmailStr = Security(try_get_valid_refresh_token),
    auth_service: AuthService = Depends(get_auth_service),
) -> ResponseToken:
    return await auth_service.refresh_token(email, response)
