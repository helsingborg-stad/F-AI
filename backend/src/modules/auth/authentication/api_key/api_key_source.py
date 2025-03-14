from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

from src.modules.auth.authentication.models.AuthenticationSourceCredentials import AuthenticationSourceCredentials
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType


def _extract_api_key(
        key: Annotated[str | None, Depends(APIKeyHeader(
            name='X-Api-Key',
            description='API Key. Can be created/revoked by an administrator.',
            auto_error=False
        ))]
) -> AuthenticationSourceCredentials:
    return AuthenticationSourceCredentials(
        auth_type=AuthenticationType.API_KEY,
        credentials=key
    )


ApiKeySource = Annotated[AuthenticationSourceCredentials, Depends(_extract_api_key)]
