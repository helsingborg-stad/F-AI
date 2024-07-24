from typing import Literal

from pydantic import BaseModel

from fai_llm.assistant.models import AssistantTemplate, AssistantStreamMessage


class WsMessages:
    class Client(BaseModel):
        command: Literal['add', 'cancel', 'query']
        job_id: str
        assistant: AssistantTemplate | None = None
        history: list[AssistantStreamMessage] = []
        query: str | None = None

    class Server(BaseModel):
        job_id: str
        status: Literal['created', 'cancelled', 'update', 'finished', 'failed']
        message: str
