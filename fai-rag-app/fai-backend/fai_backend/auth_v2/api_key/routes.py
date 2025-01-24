from fastapi import APIRouter, status
from pydantic import BaseModel

from fai_backend.auth_v2.api_key.dependencies import get_api_key_service
from fai_backend.auth_v2.api_key.models import ReadOnlyApiKeyModel
from fai_backend.auth_v2.fastapi_auth import AuthRouterDecorator

router = APIRouter(
    prefix='/api/auth',
    tags=['Auth', 'API Key']
)
auth = AuthRouterDecorator(router)


class CreateApiKeyRequest(BaseModel):
    scopes: list[str]


class CreateApiKeyResponse(BaseModel):
    key: str
    revoke_id: str


@auth.post(
    '/apikey',
    ['can_manage_api_keys'],
    response_model=CreateApiKeyResponse,
    description='''
    Create a new API key with the given scopes.
    ''',
    status_code=status.HTTP_201_CREATED,
)
async def create_api_key(body: CreateApiKeyRequest):
    service = await get_api_key_service()
    revoke_id, key = await service.create(scopes=body.scopes)
    return CreateApiKeyResponse(key=key, revoke_id=str(revoke_id))


class ListApiKeyResponse(BaseModel):
    api_keys: list[ReadOnlyApiKeyModel]


@auth.get(
    '/apikey',
    ['can_manage_api_keys'],
    response_model=ListApiKeyResponse,
    description='''
List information about all API keys.
    
Keys themselves are redacted for security purposes.
    ''',
)
async def list_api_keys():
    service = await get_api_key_service()
    keys = await service.list()
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
async def revoke_api_key(revoke_id: str):
    service = await get_api_key_service()
    await service.revoke(revoke_id)
