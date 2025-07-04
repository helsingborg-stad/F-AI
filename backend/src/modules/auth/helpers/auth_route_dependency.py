import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.authentication.api_key.api_key_source import ApiKeySource
from src.modules.auth.authentication.bearer_token.bearer_token_source import BearerTokenSource
from src.modules.auth.authentication.cookie_token.cookie_token_source import CookieTokenSource
from src.modules.auth.authentication.factory import AuthenticationServiceFactory
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authentication.models.AuthenticationSourceCredentials import AuthenticationSourceCredentials
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService
from src.modules.auth.helpers.authentication_challenge_adapter import AuthenticationChallengeAdapter


async def _get_auth_credentials(
        api_key: ApiKeySource,
        bearer_token: BearerTokenSource,
        cookie_token: CookieTokenSource
) -> AuthenticationSourceCredentials:
    credentials_priority = [api_key, bearer_token, cookie_token]

    valid_credentials_provided = [c for c in credentials_priority if
                                  c.credentials is not None and len(c.credentials) > 0]
    available_challenges = ', '.join([
        AuthenticationChallengeAdapter.to_challenge(c.auth_type) for c in credentials_priority])

    # Check for missing credentials
    if len(valid_credentials_provided) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated",
            headers={"WWW-Authenticate": available_challenges}
        )

    return valid_credentials_provided[0]


async def _authenticate(
        authentication_factory: AuthenticationServiceFactory,
        auth_type: AuthenticationType,
        auth_payload: str
) -> AuthenticatedIdentity:
    try:
        authentication_service = authentication_factory.get(auth_type)
        authenticated_credentials = await authentication_service.authenticate(auth_payload)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))
    if authenticated_credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")
    return authenticated_credentials


async def _ensure_authorized(
        authenticated_identity: AuthenticatedIdentity,
        required_scopes: list[str],
        authorization_service: IAuthorizationService
):
    valid_authorization = await authorization_service.has_scopes(authenticated_identity, required_scopes)
    if not valid_authorization:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing one or more required scopes ({', '.join(required_scopes)})"
        )


async def auth_route_dependency(
        credentials: Annotated[AuthenticationSourceCredentials, Depends(_get_auth_credentials)],
        security_scopes: SecurityScopes,
        services: ServicesDependency
) -> AuthenticatedIdentity:
    authenticated_identity = await _authenticate(
        services.authentication_factory,
        credentials.auth_type,
        credentials.credentials
    )
    await _ensure_authorized(authenticated_identity, security_scopes.scopes, services.authorization_service)

    return authenticated_identity
