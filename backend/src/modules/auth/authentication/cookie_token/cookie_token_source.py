from typing import Annotated

from fastapi import Cookie, Depends

from src.modules.auth.authentication.models.AuthenticationSourceCredentials import AuthenticationSourceCredentials
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType


def _extract_cookie_token(
        token: Annotated[str | None, Cookie(alias='access_token')] = None
) -> AuthenticationSourceCredentials:
    return AuthenticationSourceCredentials(
        auth_type=AuthenticationType.COOKIE_TOKEN,
        credentials=token,
    )


CookieTokenSource = Annotated[AuthenticationSourceCredentials, Depends(_extract_cookie_token)]
