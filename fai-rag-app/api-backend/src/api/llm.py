from fastapi import APIRouter
from pydantic import BaseModel, Field

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.llm.models.Message import Message

llm_router = APIRouter(prefix='/llm', tags=['LLM'])
auth = AuthRouterDecorator(llm_router)


class RunRequestMessage(BaseModel):
    role: str
    content: str


class RunRequest(BaseModel):
    model: str = Field(examples=['o3-mini'])
    messages: list[RunRequestMessage] = Field(examples=[[
        {"role": "system", "content": "Answer like a pirate"},
        {"role": "user", "content": "Who is the king of Sweden?"}],
    ])


class RunResponse(BaseModel):
    role: str = Field(examples=['assistant'])
    content: str = Field(examples=["""Ahoy, matey! The king o' Sweden be King Carl XVI Gustaf, 
    at the helm o' his royal ship for many a year now! Arr!"""])


@auth.post(
    '/run',
    required_scopes=['llm.run'],
    summary='Run LLM inference',
    response_model=RunResponse,
)
async def run(request: RunRequest, services: ServicesDependency):
    message = await services.llm_service.run(model=request.model, messages=[
        Message(
            role=message.role,
            content=message.content
        )
        for message in request.messages
    ])
    return RunResponse(role=message.role, content=message.content)
