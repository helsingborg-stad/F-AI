from dataclasses import field, dataclass
from datetime import datetime
from asyncio import Queue
from typing import Optional, Any, Literal, Type

from beanie import Document
from pydantic import BaseModel


class LLMClientChatMessage(BaseModel):
    date: datetime
    source: str | None = None
    content: str | None = None


class AssistantStreamMessage(BaseModel):
    role: Literal["system", "user", "assistant", "function"]
    content: str


class AssistantStreamInsert(BaseModel):
    insert: str


class AssistantStreamConfig(BaseModel):
    provider: str
    settings: dict[str, Any]
    messages: list[AssistantStreamMessage | AssistantStreamInsert]


class AssistantStreamPipelineDef(BaseModel):
    pipeline: str


class AssistantTemplateMeta(BaseModel):
    name: str = ""
    description: str = ""
    sample_questions: list[str] = []


class AssistantTemplate(BaseModel):
    id: str
    meta: AssistantTemplateMeta
    files_collection_id: Optional[str] = None
    streams: list[AssistantStreamConfig | AssistantStreamPipelineDef]


class AssistantContext(BaseModel):
    query: str = ""
    files_collection_id: Optional[str] = None
    previous_stream_output: Optional[str] = None
    history: list[AssistantStreamMessage] = []
    rag_output: Optional[str] = None


class AssistantChatHistoryModel(Document):
    history: list[AssistantStreamMessage] = []

    class Settings:
        name = 'chat_history'
        use_state_management = True


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
        'resp_add': AddResponse,
        'pending': JobPendingResponse,
        'done': JobDoneResponse,
        'failed': JobFailedResponse,
        'running': JobUpdateResponse,
    }


class GenerateRequest(BaseModel):
    id: str
    assistant: AssistantTemplate
    query: str
    history: list[AssistantStreamMessage] = []


class MessagePart(BaseModel):
    for_id: str
    part: str = ''
    is_final: bool = False


@dataclass
class ActiveRequest:
    local_id: str
    remote_id: str = ''
    ws_to_main_thread_pending_updates: Queue[MessagePart] = field(default_factory=Queue)
