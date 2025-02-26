import os

from fastapi import Depends, HTTPException, status
from fastapi.security import SecurityScopes

from src.common.services.fastapi_get_services import get_services
from src.common.services.models.Services import Services
from src.modules.auth.authentication.api_key.api_key_source_header import api_key_source_header
from src.modules.auth.authentication.factory import AuthenticationServiceFactory
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType
from src.modules.auth.helpers.authentication_challenge_adapter import AuthenticationChallengeAdapter
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService


async def _get_auth_credentials(api_key: str | None) -> (AuthenticationType, str):
    credential_types = [
        (AuthenticationType.API_KEY, api_key),
        # (AuthenticationType.BEARER_TOKEN, json.dumps(bearer_token.subject) if bearer_token else None),
    ]
    valid_credentials_provided = [(c, v) for c, v in credential_types if v is not None]
    available_challenges = ', '.join([
        AuthenticationChallengeAdapter.to_challenge(a) for a, _ in credential_types])

    # Check for missing credentials
    if len(valid_credentials_provided) == 0:
        if os.environ['DISABLE_AUTH'] == '1':
            return AuthenticationType.GUEST, ''

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated",
            headers={"WWW-Authenticate": available_challenges}
        )

    # Check for superfluous credentials
    if len(valid_credentials_provided) > 1:
        provided_credential_types = [str(c) for c, _ in valid_credentials_provided]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Too many authentication credentials provided ({'+'.join(provided_credential_types)})",
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
        security_scopes: SecurityScopes,
        api_key: str | None = Depends(api_key_source_header),
        # bearer_token: JwtAuthorizationCredentials | None = Depends(bearer_token_source),
        services: Services = Depends(get_services)
) -> AuthenticatedIdentity:
    auth_type, auth_payload = await _get_auth_credentials(api_key)
    authenticated_identity = await _authenticate(services.authentication_factory, auth_type, auth_payload)
    await _ensure_authorized(authenticated_identity, security_scopes.scopes, services.authorization_service)

    return authenticated_identity
