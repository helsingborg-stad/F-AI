import logging
import re
import random
import jwt
from collections.abc import Callable
from datetime import timedelta
from typing import Annotated

from fastapi import HTTPException, Header
from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie
from passlib.context import CryptContext

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


def is_auth_disabled() -> bool:
    return settings.ENV_MODE != 'production' and settings.DISABLE_AUTH


def read_public_key(file: str) -> str:
    with open(file, 'r') as f:
        return f.read()


def validate_key(key: str, public_key: str) -> bool:
    try:
        jwt.decode(key, public_key, algorithms=['RS256'])
        return True
    except Exception as e:
        logging.debug(msg=str(e), exc_info=True)
        return False


def authenticate(x_api_key: Annotated[str, Header()]) -> None:
    try:
        if is_auth_disabled():
            return
        if not validate_key(x_api_key, read_public_key(settings.PUBLIC_KEY_FILE)):
            raise HTTPException(status_code=401, detail='Unauthorized')
    except Exception as e:
        raise e


generate_pin_code = create_pin_factory_from_env()
