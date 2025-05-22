import base64

from fastapi import APIRouter, HTTPException, status, UploadFile
from pydantic import BaseModel

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


class GetAvailableModelsResponseModel(BaseModel):
    key: str
    provider: str
    name: str
    description: str


class GetAvailableModelsResponse(BaseModel):
    models: list[GetAvailableModelsResponseModel]


@auth.get(
    '/models',
    ['assistant.read'],
    summary='Get Available Models',
    description='''
Get a list of models that can be used with assistants.

The `model.key` should be used as an assistant's `model` value.
''',
    response_model=GetAvailableModelsResponse,
)
async def get_available_models(services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    result = await services.assistant_service.get_available_models(as_uid=auth_identity.uid)
    return GetAvailableModelsResponse(models=[
        GetAvailableModelsResponseModel(
            key=model.key,
            provider=model.provider,
            name=model.display_name,
            description=model.description
        ) for model in result
    ])


class GetAssistantResponseAssistant(BaseModel):
    name: str
    description: str
    avatar_base64: str | None
    primary_color: str | None
    sample_questions: list[str]
    allow_files: bool
    is_public: bool
    model: str
    llm_api_key: str | None
    instructions: str
    collection_id: str | None
    extra_llm_params: dict[str, float | int | bool | str]


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
            name=result.meta.name,
            description=result.meta.description,
            avatar_base64=result.meta.avatar_base64,
            primary_color=result.meta.primary_color,
            allow_files=result.meta.allow_files,
            sample_questions=result.meta.sample_questions,
            is_public=result.meta.is_public,
            model=result.model,
            llm_api_key=result.llm_api_key,
            instructions=result.instructions,
            collection_id=result.collection_id,
            extra_llm_params=result.extra_llm_params if result.extra_llm_params else {}
        )
    )


class GetAssistantInfoResponse(BaseModel):
    name: str
    description: str
    avatar_base64: str | None
    primary_color: str | None
    sample_questions: list[str]
    model: str


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
        name=result.name,
        description=result.description,
        avatar_base64=result.avatar_base64,
        primary_color=result.primary_color,
        sample_questions=result.sample_questions,
        model=result.model,
    )


class GetAvailableAssistantsResponseAssistant(BaseModel):
    id: str
    name: str
    description: str
    avatar_base64: str | None
    primary_color: str | None


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
            name=assistant.name,
            description=assistant.description,
            avatar_base64=assistant.avatar_base64,
            primary_color=assistant.primary_color,
        ) for assistant in result
    ])


class UpdateAssistantRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    primary_color: str | None = None
    allow_files: bool | None = None
    sample_questions: list[str] | None = None
    is_public: bool | None = None
    model: str | None = None
    llm_api_key: str | None = None
    instructions: str | None = None
    collection_id: str | None = None
    extra_llm_params: dict[str, float | int | bool | str] | None = None


@auth.put(
    '/{assistant_id}',
    ['assistant.write'],
    summary='Update Assistant',
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
        name=body.name,
        description=body.description,
        primary_color=body.primary_color,
        allow_files=body.allow_files,
        sample_questions=body.sample_questions,
        is_public=body.is_public,
        model=body.model,
        llm_api_key=body.llm_api_key,
        instructions=body.instructions,
        collection_id=body.collection_id,
        extra_llm_params=body.extra_llm_params,
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if body.is_public is not None:
        await services.resource_service.set_resource_visibility(as_uid=auth_identity.uid, resource=assistant_id,
                                                                public=body.is_public)


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

    base64_encoded = base64.b64encode(await file.read())
    success = await services.assistant_service.update_assistant(as_uid=auth_identity.uid, assistant_id=assistant_id,
                                                                avatar_base64=base64_encoded)

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
                                                      avatar_base64='')


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
