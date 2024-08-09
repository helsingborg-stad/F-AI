from typing import Type

from pydantic import BaseModel

from fai_llm.assistant.models import AssistantStreamMessage, AssistantTemplate


class WsMessages:
    class Base(BaseModel, extra='allow'):
        type: str

    class AddRequest(Base):
        type: str = 'add'
        id: str
        assistant: AssistantTemplate
        history: list[AssistantStreamMessage] = []
        query: str

    class ListenRequest(Base):
        type: str = 'listen'
        job_id: str

    class AddResponse(Base):
        type: str = 'resp_add'
        id: str
        job_id: str

    class JobPendingResponse(Base):
        type: str = 'pending'
        job_id: str

    class JobDoneResponse(Base):
        type: str = 'done'
        job_id: str

    class JobFailedResponse(Base):
        type: str = 'failed'
        job_id: str
        message: str

    class JobUpdateResponse(Base):
        type: str = 'running'
        job_id: str
        message: str

    incoming_type_map: dict[str, Type[Base]] = {
        'add': AddRequest,
        'listen': ListenRequest,
    }
