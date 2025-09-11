from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.models.models.Model import Model

model_router = APIRouter(
    prefix='/model',
    tags=['Model']
)

auth = AuthRouterDecorator(model_router)


class ModelResponse(BaseModel):
    key: str
    provider: str
    display_name: str
    description: str | None = None
    meta: dict = Field(default_factory=dict)
    status: str
    visibility: str
    version: int
    created_at: str
    updated_at: str


class CreateModelRequest(BaseModel):
    key: str
    provider: str
    display_name: str
    description: str | None = None
    meta: dict = Field(default_factory=dict)
    status: str = 'active'
    visibility: str = 'public'


@auth.post(
    '/',
    ['model.write'],
    summary='Create Model',
    description='Create a new AI model for use with assistants.',
    response_model=ModelResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_model(
        request: CreateModelRequest,
        services: ServicesDependency,
        auth_identity: AuthenticatedIdentity
):
    model = Model(
        key=request.key,
        provider=request.provider,
        display_name=request.display_name,
        description=request.description,
        meta=request.meta,
        status=request.status,
        visibility=request.visibility
    )

    success = await services.model_service.create_model(model, auth_identity.uid)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Model with key '{request.key}' already exists or creation failed"
        )

    created_model = await services.model_service.get_model(request.key, auth_identity.uid)
    if not created_model:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model was created but could not be retrieved"
        )

    return ModelResponse(
        key=created_model.key,
        provider=created_model.provider,
        display_name=created_model.display_name,
        description=created_model.description,
        meta=created_model.meta,
        status=created_model.status,
        visibility=created_model.visibility,
        version=created_model.version,
        created_at=created_model.created_at.isoformat(),
        updated_at=created_model.updated_at.isoformat()
    )


class GetModelsResponse(BaseModel):
    models: list[ModelResponse]


@auth.get(
    '/',
    ['model.read'],
    summary='List All Models',
    description='Get a list of all models (including disabled/deprecated for admins).',
    response_model=GetModelsResponse
)
async def list_models(services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    models = await services.model_service.get_available_models(auth_identity.uid)

    return GetModelsResponse(
        models=[
            ModelResponse(
                key=model.key,
                provider=model.provider,
                display_name=model.display_name,
                description=model.description,
                meta=model.meta,
                status=model.status,
                visibility=model.visibility,
                version=model.version,
                created_at=model.created_at.isoformat(),
                updated_at=model.updated_at.isoformat()
            )
            for model in models
        ]
    )


@auth.get(
    '/{key:path}',
    ['model.read'],
    summary='Get Model',
    description='Get a specific model by key.',
    response_model=ModelResponse
)
async def get_model(
        key: str,
        services: ServicesDependency,
        auth_identity: AuthenticatedIdentity
):
    model = await services.model_service.get_model(key, auth_identity.uid)

    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model with key '{key}' not found"
        )

    return ModelResponse(
        key=model.key,
        provider=model.provider,
        display_name=model.display_name,
        description=model.description,
        meta=model.meta,
        status=model.status,
        visibility=model.visibility,
        version=model.version,
        created_at=model.created_at.isoformat(),
        updated_at=model.updated_at.isoformat()
    )


class UpdateModelRequest(BaseModel):
    provider: str
    display_name: str
    description: str | None = None
    meta: dict = Field(default_factory=dict)
    status: str = 'active'
    visibility: str = 'public'
    version: int


@auth.put(
    '/{key:path}',
    ['model.write'],
    summary='Update Model',
    description='Update an existing model with optimistic locking.',
    response_model=ModelResponse
)
async def update_model(
        key: str,
        request: UpdateModelRequest,
        services: ServicesDependency,
        auth_identity: AuthenticatedIdentity
):
    model = Model(
        key=key,
        provider=request.provider,
        display_name=request.display_name,
        description=request.description,
        meta=request.meta,
        status=request.status,
        visibility=request.visibility,
        version=request.version
    )

    success = await services.model_service.update_model(key, model, auth_identity.uid)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Model with key '{key}' not found or version mismatch (concurrent update)"
        )

    updated_model = await services.model_service.get_model(key, auth_identity.uid)
    if not updated_model:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Model was updated but could not be retrieved"
        )

    return ModelResponse(
        key=updated_model.key,
        provider=updated_model.provider,
        display_name=updated_model.display_name,
        description=updated_model.description,
        meta=updated_model.meta,
        status=updated_model.status,
        visibility=updated_model.visibility,
        version=updated_model.version,
        created_at=updated_model.created_at.isoformat(),
        updated_at=updated_model.updated_at.isoformat()
    )


@auth.delete(
    '/{key:path}',
    ['model.write'],
    summary='Delete Model',
    description='Delete a model (only if not in use by any assistants).',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_model(
        key: str,
        services: ServicesDependency,
        auth_identity: AuthenticatedIdentity
):
    success = await services.model_service.delete_model(key, auth_identity.uid)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Model with key '{key}' not found or is in use by assistants"
        )
