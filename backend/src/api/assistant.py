import base64
from typing import Any

from fastapi import APIRouter, HTTPException, status, UploadFile
from pydantic import BaseModel, Field

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity

assistant_router = APIRouter(
    prefix='/assistant',
    tags=['Assistant']
)

auth = AuthRouterDecorator(assistant_router)


class CreateAssistantResponse(BaseModel):
    assistant_id: str


@auth.post(
    '',
    ['assistant.write'],
    summary='Create Assistant',
    response_model=CreateAssistantResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_assistant(services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    new_id = await services.assistant_service.create_assistant(as_uid=auth_identity.uid)
    return CreateAssistantResponse(assistant_id=new_id)


class GetMyAssistantsResponseAssistant(BaseModel):
    id: str
    meta: dict[str, Any]


class GetMyAssistantsResponse(BaseModel):
    assistants: list[GetMyAssistantsResponseAssistant]


@auth.get(
    '/me',
    ['assistant.read'],
    summary='Get My Assistants',
    response_model=GetMyAssistantsResponse,
)
async def get_my_assistants(services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    result = await services.assistant_service.get_owned_assistants(as_uid=auth_identity.uid)
    return GetMyAssistantsResponse(assistants=[
        GetMyAssistantsResponseAssistant(
            id=assistant.id,
            meta=assistant.meta,
        ) for assistant in result
    ])


class GetAvailableAssistantsResponseAssistant(BaseModel):
    id: str
    meta: dict[str, Any]


class GetAvailableAssistantsResponse(BaseModel):
    assistants: list[GetAvailableAssistantsResponseAssistant]


@auth.get(
    '',
    ['assistant.read'],
    summary='Get Available Assistants',
    response_model=GetAvailableAssistantsResponse,
)
async def get_available_assistants(services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    result = await services.assistant_service.get_available_assistants(as_uid=auth_identity.uid)
    return GetAvailableAssistantsResponse(assistants=[
        GetAvailableAssistantsResponseAssistant(
            id=assistant.id,
            meta=assistant.meta
        ) for assistant in result
    ])


@auth.post(
    '/me/favorite/{assistant_id}',
    ['assistant.read'],
    summary='Add favorite assistant'
)
async def add_favorite_assistant(assistant_id: str, services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    success = await services.assistant_service.set_assistant_as_favorite(as_uid=auth_identity.uid,
                                                                         assistant_id=assistant_id)

    if success is False:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


class GetFavoriteAssistantsResponseAssistant(BaseModel):
    id: str
    meta: dict[str, Any]


class GetFavoriteAssistantsResponse(BaseModel):
    assistants: list[GetFavoriteAssistantsResponseAssistant]


@auth.get(
    '/me/favorite',
    summary='Get favorite assistants',
    response_model=GetFavoriteAssistantsResponse
)
async def get_favorite_assistants(services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    result = await services.assistant_service.get_favorite_assistants(as_uid=auth_identity.uid)
    return GetFavoriteAssistantsResponse(
        assistants=[GetFavoriteAssistantsResponseAssistant(
            id=assistant.id,
            meta=assistant.meta
        ) for assistant in result]
    )


class RemoveFavoriteAssistantRequest(BaseModel):
    assistant_id: str


@auth.delete(
    '/me/favorite/{assistant_id}',
    summary='Remove favorite assistant',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_favorite_assistant(assistant_id: str, services: ServicesDependency,
                                    auth_identity: AuthenticatedIdentity):
    await services.assistant_service.remove_assistant_as_favorite(as_uid=auth_identity.uid, assistant_id=assistant_id)


class GetAssistantResponseAssistant(BaseModel):
    meta: dict[str, Any]
    model: str
    llm_api_key: str | None
    instructions: str
    collection_id: str | None
    max_collection_results: int
    extra_llm_params: dict


class GetAssistantResponse(BaseModel):
    assistant: GetAssistantResponseAssistant


@auth.get(
    '/{assistant_id}',
    ['assistant.read'],
    summary='Get Assistant',
    response_model=GetAssistantResponse,
    response_404_description='Assistant not found',
)
async def get_assistant(assistant_id: str, services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    result = await services.assistant_service.get_assistant(as_uid=auth_identity.uid, assistant_id=assistant_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    # if not result.owner == auth_identity.uid:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return GetAssistantResponse(
        assistant=GetAssistantResponseAssistant(
            meta=result.meta,
            model=result.model,
            llm_api_key=result.llm_api_key,
            instructions=result.instructions,
            collection_id=result.collection_id,
            max_collection_results=result.max_collection_results,
            extra_llm_params=result.extra_llm_params if result.extra_llm_params else {}
        )
    )


class GetAssistantInfoResponse(BaseModel):
    model: str
    meta: dict[str, Any]


@auth.get(
    '/{assistant_id}/info',
    ['assistant.read'],
    summary='Get Assistant Info',
    response_model=GetAssistantInfoResponse,
    response_404_description='Assistant not found',
)
async def get_assistant_info(assistant_id: str, services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    result = await services.assistant_service.get_assistant_info(as_uid=auth_identity.uid, assistant_id=assistant_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return GetAssistantInfoResponse(
        meta=result.meta,
        model=result.model,
    )


class UpdateAssistantRequest(BaseModel):
    meta: dict[str, Any] | None = Field(default=None, examples=[{'name': 'my assistant'}])
    model: str | None = Field(default=None, examples=['openai:o3-mini'])
    llm_api_key: str | None = Field(default=None, examples=['sk-proj-abc123'])
    instructions: str | None = Field(default=None, examples=['Answer in Swedish.'])
    collection_id: str | None = Field(default=None, examples=['my-collection-id'])
    max_collection_results: int | None = None
    extra_llm_params: dict | None = Field(default=None, examples=[{}])


@auth.put(
    '/{assistant_id}',
    ['assistant.write'],
    summary='Update Assistant',
    description='''
Update an assistant. 

Note that `meta` is a generic key-value store and can contain any data.
It contains any data not needed for the assistant itself to run, such as
frontend-specific details (name, description, image etc.).

`extra_llm_params` is also a generic key-value store and is model-specific.
It may contain properties such as `temperature` for certain models.
''',
    response_404_description='Assistant not found',
)
async def update_assistant(
        assistant_id: str,
        body: UpdateAssistantRequest,
        services: ServicesDependency,
        auth_identity: AuthenticatedIdentity
):
    success = await services.assistant_service.update_assistant(
        as_uid=auth_identity.uid,
        assistant_id=assistant_id,
        meta=body.meta,
        model=body.model,
        llm_api_key=body.llm_api_key,
        instructions=body.instructions,
        collection_id=body.collection_id,
        max_collection_results=body.max_collection_results,
        extra_llm_params=body.extra_llm_params,
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if body.meta and 'is_public' in body.meta and isinstance(body.meta['is_public'], bool):
        await services.resource_service.set_resource_visibility(as_uid=auth_identity.uid, resource=assistant_id,
                                                                public=body.meta['is_public'])


@auth.put(
    '/{assistant_id}/avatar',
    ['assistant.write'],
    summary='Update Assistant Avatar',
    description='Update an assistants avatar image. PNG only. Max size 1 MB.',
    response_404_description='Assistant not found',
)
async def update_assistant_avatar(assistant_id: str, file: UploadFile, services: ServicesDependency,
                                  auth_identity: AuthenticatedIdentity):
    if not file.content_type == 'image/png':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid file type')

    if file.size > 1024 * 1024:  # 1 Mb
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='File too large')

    base64_encoded = base64.b64encode(await file.read()).decode('utf-8')
    success = await services.assistant_service.update_assistant(as_uid=auth_identity.uid, assistant_id=assistant_id,
                                                                meta={'avatar_base64': base64_encoded})

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@auth.delete(
    '/{assistant_id}/avatar',
    ['assistant.write'],
    summary='Delete Assistant Avatar',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_assistant_avatar(assistant_id: str, services: ServicesDependency,
                                  auth_identity: AuthenticatedIdentity):
    await services.assistant_service.update_assistant(as_uid=auth_identity.uid, assistant_id=assistant_id,
                                                      meta={'avatar_base64': None})


class DeleteAssistantRequest(BaseModel):
    assistant_id: str


@auth.delete(
    '/{assistant_id}',
    ['assistant.write'],
    summary='Delete Assistant',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_assistant(assistant_id: str, services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    await services.assistant_service.delete_assistant(as_uid=auth_identity.uid, assistant_id=assistant_id)
