from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.modules.auth.authentication.models.AuthenticationSourceCredentials import AuthenticationSourceCredentials
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType


def _extract_bearer_token(
        token: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer(
            scheme_name='Bearer Token',
            description='JWT Token associated with an authenticated user.',
            auto_error=False
        ))]
) -> AuthenticationSourceCredentials:
    return AuthenticationSourceCredentials(
        auth_type=AuthenticationType.BEARER_TOKEN,
        credentials=token.credentials if token else None
    )


BearerTokenSource = Annotated[AuthenticationSourceCredentials, Depends(_extract_bearer_token)]
