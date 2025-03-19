from fastapi import APIRouter, status
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.api_key.models.RedactedApiKey import RedactedApiKey
from src.modules.auth.auth_router_decorator import AuthRouterDecorator

api_key_router = APIRouter(
    prefix='/apikey',
    tags=['API Key']
)

auth = AuthRouterDecorator(api_key_router)


class CreateApiKeyResponse(BaseModel):
    key: str
    revokeId: str


@auth.post(
    '',
    ['apiKey.write'],
    summary='Create API Key',
    description='''
    Create a new API key.
    ''',
    status_code=status.HTTP_201_CREATED,
    response_model=CreateApiKeyResponse
)
async def create_api_key(services: ServicesDependency):
    new_key = await services.api_key_service.create_api_key()
    return CreateApiKeyResponse(key=new_key.api_key, revokeId=new_key.revoke_id)


class ListApiKeyResponse(BaseModel):
    api_keys: list[RedactedApiKey]


@auth.get(
    '',
    ['apiKey.read'],
    description='''
List information about all API keys.

Keys themselves are redacted for security reasons.
    ''',
    response_model=ListApiKeyResponse,
)
async def list_api_keys(services: ServicesDependency):
    keys = await services.api_key_service.get_api_keys()
    return ListApiKeyResponse(api_keys=keys)


@auth.delete(
    '/apikey/{revoke_id}',
    ['apiKey.write'],
    description='''
Revoke a specific API key (permanently delete it).

The `revoke_id` can be found through the `create` and `list` operations.
    ''',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def revoke_api_key(revoke_id: str, services: ServicesDependency):
    await services.api_key_service.revoke_api_key(revoke_id)
