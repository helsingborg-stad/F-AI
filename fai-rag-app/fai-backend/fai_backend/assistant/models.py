from typing import Optional, Any, Literal

from beanie import Document
from pydantic import BaseModel


class LLMClientChatMessage(BaseModel):
    timestamp: str
    source: str | None = None
    content: str | None = None


class AssistantStreamMessage(BaseModel):
    timestamp: str = ""
    role: Literal["system", "user", "assistant", "function"]
    content: str
    should_format: bool = False


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


class ClientChatState(BaseModel):
    chat_id: str
    timestamp: str
    title: str
    history: list[LLMClientChatMessage]


class AssistantChatHistoryModel(Document):
    user: str
    assistant: AssistantTemplate
    history: list[AssistantStreamMessage] = []

    class Settings:
        name = 'chat_history'
        use_state_management = True


class ClientChatState(BaseModel):
    id: str
    timestamp: str
    title: str
    history: list[LLMClientChatMessage]
