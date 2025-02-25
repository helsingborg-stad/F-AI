from fastapi import APIRouter, status, HTTPException
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.api_key.models.RedactedApiKey import RedactedApiKey
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity

api_key_router = APIRouter(
    prefix='/apikey',
    tags=['API Key']
)

auth = AuthRouterDecorator(api_key_router)


class CreateApiKeyRequest(BaseModel):
    scopes: list[str]


class CreateApiKeyResponse(BaseModel):
    key: str
    revokeId: str


@auth.post(
    '',
    ['can_manage_api_keys'],
    summary='Create API Key',
    description='''
    Create a new API key with the given scopes.
    ''',
    status_code=status.HTTP_201_CREATED,
    response_model=CreateApiKeyResponse,
    response_400_description='No scopes provided.'
)
async def create_api_key(body: CreateApiKeyRequest, auth_identity: AuthenticatedIdentity,
                         services: ServicesDependency):
    desired_scopes = [scope for scope in body.scopes if len(scope) > 0]

    if len(desired_scopes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No scopes provided.'
        )

    if not await services.authorization_service.has_scopes(auth_identity, desired_scopes):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Can not assign scope(s) outside of creator's scopes to an API key."
        )

    new_key = await services.api_key_service.create(scopes=desired_scopes)
    return CreateApiKeyResponse(key=new_key.api_key, revokeId=new_key.revoke_id)


class ListApiKeyResponse(BaseModel):
    api_keys: list[RedactedApiKey]


@auth.get(
    '',
    ['can_manage_api_keys'],
    description='''
List information about all API keys.

Keys themselves are redacted for security reasons.
    ''',
    response_model=ListApiKeyResponse,
)
async def list_api_keys(services: ServicesDependency):
    keys = await services.api_key_service.get_all()
    return ListApiKeyResponse(api_keys=keys)


@auth.delete(
    '/apikey/{revoke_id}',
    ['can_manage_api_keys'],
    description='''
Revoke a specific API key (permanently delete it).

The `revoke_id` can be found through the `create` and `list` operations.
    ''',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def revoke_api_key(revoke_id: str, services: ServicesDependency):
    await services.api_key_service.revoke(revoke_id)
