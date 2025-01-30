import inspect
import json
from functools import partial
from typing import Callable, Any

from fastapi import Depends, HTTPException, status, APIRouter, Security
from fastapi.security import SecurityScopes
from fastapi_jwt import JwtAuthorizationCredentials
from pydantic import BaseModel

from fai_backend.auth_v2.authentication.factory import AuthenticationFactory
from fai_backend.auth_v2.authentication.fastapi_sources import api_key_source, bearer_token_source
from fai_backend.auth_v2.authentication.models import AuthenticationType, AuthenticatedIdentity
from fai_backend.auth_v2.authorization.factory import AuthorizationFactory
from fai_backend.config import settings


class CommonHTTPErrorResponse(BaseModel):
    detail: str


class AuthenticationChallengeAdapter:
    @staticmethod
    def to_challenge(authentication_method: str) -> str:
        mapping: dict[str, str] = {
            AuthenticationType.API_KEY: 'Api-Key realm="main"',
            AuthenticationType.BEARER_TOKEN: 'Bearer realm="main"',
        }
        return mapping.get(authentication_method, f'{authentication_method} realm="main"')


auth_responses = {
    400: {
        "description": "(Auth) too many credentials provided; only one type should be used.",
        "model": CommonHTTPErrorResponse,
        "content": {
            "application/json": {
                "example": CommonHTTPErrorResponse(
                    detail="Too many authentication credentials provided (x+y)"
                )
            }
        }
    },
    401: {
        "description": '''No credentials provided or provided credentials are invalid (e.g. expired).
                        \nAvailable authentication methods are provided in the WWW-Authenticate header.''',
        "model": CommonHTTPErrorResponse,
        "content": {
            "application/json": {
                "example": CommonHTTPErrorResponse(
                    detail="Not Authenticated"
                )
            }
        }

    },
    403: {
        "description": "Credentials are missing one or more required scopes (operation permissions).",
        "model": CommonHTTPErrorResponse,
        "content": {
            "application/json": {
                "example": CommonHTTPErrorResponse(
                    detail="Missing one or more required scopes (x, y, z)"
                )
            }
        }
    },
}


async def auth_dependency(
        security_scopes: SecurityScopes,
        api_key: str | None = Depends(api_key_source),
        bearer_token: JwtAuthorizationCredentials | None = Depends(bearer_token_source),
) -> AuthenticatedIdentity:
    if settings.HTTP_AUTHENTICATION_TYPE == 'none':
        return AuthenticatedIdentity(uid='')

    credential_types = [
        (AuthenticationType.API_KEY, api_key),
        (AuthenticationType.BEARER_TOKEN, json.dumps(bearer_token.subject) if bearer_token else None),
    ]

    valid_credentials_provided = [(c, v) for c, v in credential_types if v is not None]

    available_challenges = ', '.join([
        AuthenticationChallengeAdapter.to_challenge(a) for a, _ in credential_types])

    # Check for missing credentials
    if len(valid_credentials_provided) == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated",
            headers={"WWW-Authenticate": available_challenges}
        )

    # Check for superfluous credentials
    if len(valid_credentials_provided) > 1:
        provided_credential_types = [c for c, _ in valid_credentials_provided]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Too many authentication credentials provided ({'+'.join(provided_credential_types)})",
            headers={"WWW-Authenticate": available_challenges}
        )

    # Check for valid credentials
    auth_type, auth_payload = valid_credentials_provided[0]
    try:
        authentication_provider = await AuthenticationFactory.get(auth_type)
        authenticated_credentials = await authentication_provider.validate(auth_payload)
    except ValueError as ex:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(ex))

    if authenticated_credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials")

    # Check for valid permissions
    required_scopes = security_scopes.scopes
    authorization_provider = await AuthorizationFactory.get()
    valid_authorization = await authorization_provider.has_scopes(authenticated_credentials, required_scopes)

    if not valid_authorization:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing one or more required scopes ({', '.join(required_scopes)})"
        )

    return authenticated_credentials


def get_auth_responses(additional_400_description: str | None = None) -> dict[int, dict]:
    result = dict(auth_responses)

    if additional_400_description:
        result[400]["description"] = f"{additional_400_description}\n\n{auth_responses[400]['description']}"

    return result


def make_auth_path_description(path_description: str, scopes: list[str]) -> str:
    if len(scopes) == 0:
        return f'{path_description}\n\n*__(Auth) no scopes required__*'
    return f'{path_description}\n\n*__(Auth) required scope(s): {", ".join(scopes)}__*'


class AuthRouterDecorator:
    def __init__(self, api_router: APIRouter):
        self.api_router = api_router

    @staticmethod
    def route(
            router_method: Callable,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            status_code: int | None = None,
    ):
        if required_scopes is None:
            required_scopes = []

        def inner_decorator(func):
            security_dependency = Security(auth_dependency, scopes=required_scopes)
            parameters = inspect.signature(func).parameters
            function_has_identity_parameter = 'auth_identity' in parameters
            fn = partial(func,
                         auth_identity=security_dependency) if function_has_identity_parameter else func
            deps = [] if function_has_identity_parameter else [security_dependency]

            router_method(
                path,
                summary=summary,
                description=make_auth_path_description(description, scopes=required_scopes),
                response_model=response_model,
                response_description=response_description,
                responses=get_auth_responses(response_400_description),
                dependencies=deps,
                status_code=status_code,
            )(fn)

        return inner_decorator

    def get(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.get,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            status_code=status_code,
        )

    def post(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.post,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            status_code=status_code,
        )

    def put(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.put,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            status_code=status_code,
        )

    def patch(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.patch,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            status_code=status_code,
        )

    def delete(
            self,
            path: str,
            required_scopes: list[str] = None,
            summary: str | None = None,
            description: str | None = None,
            response_model: Any | None = None,
            response_description: str | None = None,
            response_400_description: str | None = None,
            status_code: int | None = None,
    ):
        return AuthRouterDecorator.route(
            router_method=self.api_router.delete,
            path=path,
            required_scopes=required_scopes,
            summary=summary,
            description=description,
            response_model=response_model,
            response_description=response_description,
            response_400_description=response_400_description,
            status_code=status_code,
        )
