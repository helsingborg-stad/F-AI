from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.common.services.fastapi_get_services import get_services
from src.common.services.models.Services import Services
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.llm.models.Message import Message

llm_router = APIRouter(prefix='/llm', tags=['LLM'])
auth = AuthRouterDecorator(llm_router)


class RunRequestMessage(BaseModel):
    role: str
    content: str


class RunRequest(BaseModel):
    model: str
    messages: list[RunRequestMessage]


class RunResponse(BaseModel):
    role: str
    content: str


@auth.post('/run', required_scopes=['can_ask_questions'])
async def run(request: RunRequest, services: Annotated[Services, Depends(get_services)]):
    message = await services.llm_service.run(model=request.model, messages=[
        Message(
            role=message.role,
            content=message.content
        )
        for message in request.messages
    ])
    return RunResponse(role=message.role, content=message.content)
