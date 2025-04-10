from fastapi import APIRouter, HTTPException, status
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


class GetAssistantResponseAssistant(BaseModel):
    name: str
    description: str
    sample_questions: list[str]
    allow_files: bool
    model: str
    llm_api_key: str | None
    instructions: str
    temperature: float
    max_tokens: int
    collection_id: str | None


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

    return GetAssistantResponse(
        assistant=GetAssistantResponseAssistant(
            name=result.meta.name,
            description=result.meta.description,
            allow_files=result.meta.allow_files,
            sample_questions=result.meta.sample_questions,
            model=result.model,
            llm_api_key=result.llm_api_key,
            instructions=result.instructions,
            temperature=result.temperature,
            max_tokens=result.max_tokens,
            collection_id=result.collection_id
        )
    )


class GetAvailableAssistantsResponseAssistant(BaseModel):
    id: str
    owner: str
    name: str
    description: str


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
            owner=assistant.owner,
            name=assistant.meta.name,
            description=assistant.meta.description,
        ) for assistant in result
    ])


class UpdateAssistantRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    allow_files: bool | None = None
    sample_questions: list[str] | None = None
    model: str | None = None
    llm_api_key: str | None = None
    instructions: str | None = None
    temperature: float | None = None
    max_tokens: int | None = None
    collection_id: str | None = None


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
        allow_files=body.allow_files,
        sample_questions=body.sample_questions,
        model=body.model,
        llm_api_key=body.llm_api_key,
        instructions=body.instructions,
        temperature=body.temperature,
        max_tokens=body.max_tokens,
        collection_id=body.collection_id,
    )

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


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
