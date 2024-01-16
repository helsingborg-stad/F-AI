import random
from datetime import timedelta

from fastapi_jwt import JwtAccessBearerCookie, JwtRefreshBearerCookie
from passlib.context import CryptContext

from fai_backend.config import settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

access_security = JwtAccessBearerCookie(
    secret_key='SECRET_KEY',
    auto_error=False,
    access_expires_delta=timedelta(hours=12),
)

refresh_security = JwtRefreshBearerCookie(
    secret_key='SECRET_KEY',
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


def create_pin_factory_from_env():
    return (
        lambda: str(settings.FIXED_PIN) if settings.FIXED_PIN else lambda: str(random.randint(1000, 9999))
    )


generate_pin_code = create_pin_factory_from_env()
