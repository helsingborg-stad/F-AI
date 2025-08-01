from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.llm.helpers.collect_streamed import collect_streamed
from src.modules.llm.models.Message import Message
from src.modules.llm.protocols.ILLMService import ILLMService

llm_router = APIRouter(prefix='/llm', tags=['LLM'])
auth = AuthRouterDecorator(llm_router)


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


class RunResponse(BaseModel):
    role: str = Field(examples=['assistant'])
    content: str | None = Field(examples=["""Ahoy, matey! The king o' Sweden be King Carl XVI Gustaf, 
    at the helm o' his royal ship for many a year now! Arr!"""])


@auth.post(
    '/run',
    required_scopes=['llm.run'],
    summary='Run LLM inference',
    response_model=RunResponse,
)
async def run(request: RunRequest, services: ServicesDependency):
    try:
        service: ILLMService = services.llm_factory.get()
        message = await collect_streamed(service.run(
            model=request.model,
            messages=[
                Message(
                    role=message.role,
                    content=message.content
                )
                for message in request.messages
            ],
            api_key=request.api_key if request.api_key else "",
            enabled_features=[],
            extra_params=request.extra_params if request.extra_params else {}
        ))

        return RunResponse(role=message.role, content=message.content)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
