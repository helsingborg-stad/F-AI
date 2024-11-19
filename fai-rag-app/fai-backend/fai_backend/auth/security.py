import logging
import random
import re
from collections.abc import Callable
from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie
from passlib.context import CryptContext
from starlette.requests import Request

from fai_backend.auth.http_bearer_factory import ApiCredentialsFactory
from fai_backend.auth.schema import CustomHTTPAuthorizationCredentials
from fai_backend.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

access_security = JwtAccessBearerCookie(
    secret_key=settings.SECRET_KEY.get_secret_value(),
    auto_error=False,
    access_expires_delta=timedelta(hours=12),
)

refresh_security = JwtRefreshBearerCookie(
    secret_key=settings.SECRET_KEY.get_secret_value(),
    auto_error=True,
    refresh_expires_delta=timedelta(days=2),
)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(subject: dict):
    return access_security.create_access_token(subject=subject)


def create_refresh_token(subject: dict):
    return refresh_security.create_refresh_token(subject=subject)


def create_pin_factory_from_env() -> Callable[[], str]:
    return (lambda: str(settings.FIXED_PIN)) if settings.FIXED_PIN else (lambda: str(random.randint(1000, 9999)))


def is_mail_pattern(email: str) -> bool:
    return '*' in email


def try_match_email(email: str, pattern: str) -> bool:
    def pattern_to_regex(p: str) -> str:
        escaped = re.escape(p).replace(r'\*', '.*')
        return f'^{escaped}$'

    if is_mail_pattern(email):
        return False

    if '@' not in pattern:
        raise ValueError('Pattern must contain @')

    pattern_local, pattern_domain = pattern.split('@')
    email_local, email_domain = email.split('@')

    local_regex = pattern_to_regex(pattern_local)
    domain_regex = pattern_to_regex(pattern_domain)

    if re.match(local_regex, email_local) and re.match(domain_regex, email_domain):
        return True

    return False


async def get_api_credentials(r: Request) -> CustomHTTPAuthorizationCredentials:
    api_credentials = ApiCredentialsFactory.create(settings.HTTP_AUTHENTICATION_TYPE)
    return await api_credentials.create(r)


def get_public_key() -> str:
    return settings.PUBLIC_KEY


def validate_token_adapter(token: str, public_key: str, algorithm: str) -> bool:
    try:
        jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
        return True
    except Exception as e:
        logging.info(e)
        return False


async def authenticate_api_access(
        credentials: Annotated[CustomHTTPAuthorizationCredentials, Depends(get_api_credentials)]) -> None:
    if credentials.is_disabled:
        return None

    if not validate_token_adapter(credentials.credentials, get_public_key(), settings.JWT_DECODE_ALGORITHM):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def check_permissions(
        required: list[str],
        actual: list[str]
):
    for permission in required:
        if permission not in actual:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


generate_pin_code = create_pin_factory_from_env()
