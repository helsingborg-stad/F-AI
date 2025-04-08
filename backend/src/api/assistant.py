from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator

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
    response_model=CreateAssistantResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_assistant(services: ServicesDependency):
    new_id = await services.assistant_service.create_assistant()
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
    response_model=GetAssistantResponse,
    response_404_description='Assistant not found',
)
async def get_assistant(assistant_id: str, services: ServicesDependency):
    result = await services.assistant_service.get_assistant(assistant_id)

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


class GetAssistantsResponseAssistant(BaseModel):
    id: str
    name: str
    description: str


class GetAssistantsResponse(BaseModel):
    assistants: list[GetAssistantsResponseAssistant]


@auth.get(
    '',
    ['assistant.read'],
    response_model=GetAssistantsResponse,
)
async def get_assistants(services: ServicesDependency):
    result = await services.assistant_service.get_assistants()
    return GetAssistantsResponse(assistants=[
        GetAssistantsResponseAssistant(
            id=assistant.id,
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
    response_404_description='Assistant not found',
)
async def update_assistant(assistant_id: str, body: UpdateAssistantRequest, services: ServicesDependency):
    success = await services.assistant_service.update_assistant(
        assistant_id,
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
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_assistant(assistant_id: str, services: ServicesDependency):
    await services.assistant_service.delete_assistant(assistant_id)
