from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.ai.completions.models.Feature import features_from_string
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.ai.completions.helpers.collect_streamed import collect_streamed
from src.modules.ai.completions.models.Message import Message
from src.modules.ai.completions.protocols.ICompletionsService import ICompletionsService

ai_router = APIRouter(prefix='/ai', tags=['AI'])
auth = AuthRouterDecorator(ai_router)


class RunRequestMessage(BaseModel):
    role: str
    content: str


class RunRequest(BaseModel):
    model: str = Field(examples=['openai:o3-mini'])
    messages: list[RunRequestMessage] = Field(examples=[[
        {"role": "system", "content": "Answer like a pirate"},
        {"role": "user", "content": "Who is the king of Sweden?"}],
    ])
    api_key: str | None = Field(default=None, examples=['my-api-key'])
    extra_params: dict | None = Field(default=None, examples=[{'temperature': 0.5}])
    enabled_features: list[str] | None = Field(default=None, examples=[['IMAGE_GEN']])


class RunResponse(BaseModel):
    role: str = Field(examples=['assistant'])
    content: str | None = Field(examples=["""Ahoy, matey! The king o' Sweden be King Carl XVI Gustaf, 
    at the helm o' his royal ship for many a year now! Arr!"""])


@auth.post(
    '/completions',
    required_scopes=['ai.run'],
    summary='Run LLM completions',
    response_model=RunResponse,
)
async def completions(request: RunRequest, services: ServicesDependency):
    try:
        service: ICompletionsService = services.completions_factory.get(model=request.model,
                                                                        api_key=request.api_key if request.api_key else "")
        message = await collect_streamed(service.run_completions(
            messages=[
                Message(
                    role=message.role,
                    content=message.content
                )
                for message in request.messages
            ],
            enabled_features=features_from_string(
                ",".join(request.enabled_features)) if request.enabled_features else [],
            extra_params=request.extra_params if request.extra_params else {}
        ))

        return RunResponse(role=message.role, content=message.content)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
