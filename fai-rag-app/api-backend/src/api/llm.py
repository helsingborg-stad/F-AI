from fastapi import APIRouter
from pydantic import BaseModel
from src.modules.llm.factory import LLMFactory
from src.modules.llm.models.Message import Message

router = APIRouter(prefix='/llm', tags=['LLM'])


class RunRequestMessage(BaseModel):
    role: str
    content: str


class RunRequest(BaseModel):
    model: str
    messages: list[RunRequestMessage]


class RunResponse(BaseModel):
    role: str
    content: str


@router.post('/run', response_model=RunResponse)
async def run(request: RunRequest):
    service = await LLMFactory().get()
    message = await service.run(model=request.model, messages=[
        Message(
            role=message.role,
            content=message.content
        )
        for message in request.messages
    ])
    return RunResponse(role=message.role, content=message.content)
