from typing import Literal, Type, Callable, Awaitable

from pydantic import BaseModel

from fai_llm.assistant.models import AssistantTemplate, AssistantStreamMessage


class WorkStatus(BaseModel):
    status: Literal['pending', 'running', 'cancelled', 'done', 'failed']
    message: str = ''


class WorkerMessages:
    class Base(BaseModel, extra='allow'):
        type: str

    class AddRequest(Base):
        type: str = 'add'
        job_id: str
        assistant: AssistantTemplate
        history: list[AssistantStreamMessage]
        query: str

    class JobUpdate(Base):
        type: str = 'update'
        job_id: str
        message: str

    class JobDone(Base):
        type: str = 'done'
        job_id: str

    class JobError(Base):
        type: str = 'error'
        job_id: str
        error: str

    type_map: dict[str, Type[Base]] = {
        'add': AddRequest,
        'update': JobUpdate,
        'done': JobDone,
        'error': JobError,
    }


WorkCallback = Callable[[WorkerMessages.Base], Awaitable[None]]
