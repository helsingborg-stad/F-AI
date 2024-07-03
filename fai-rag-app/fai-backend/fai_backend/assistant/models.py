from datetime import datetime
from typing import Optional, Any, Literal

from pydantic import BaseModel


class LLMClientChatMessage(BaseModel):
    date: datetime
    source: str | None = None
    content: str | None = None


class AssistantStreamMessage(BaseModel):
    role: Literal["system", "user", "assistant", "function"]
    content: str


class AssistantContext(BaseModel):
    query: str = ""
    files_collection_id: Optional[str] = None
    previous_stream_output: Optional[str] = None
    history: list[AssistantStreamMessage] = []
    rag_output: Optional[str] = None


class AssistantTemplateMeta(BaseModel):
    name: str = ""
    description: str = ""
    sample_questions: list[str] = []


class AssistantStreamConfig(BaseModel):
    provider: str
    settings: dict[str, Any]
    messages: list[AssistantStreamMessage]


class AssistantStreamPipelineDef(BaseModel):
    pipeline: str


class AssistantTemplate(BaseModel):
    id: str
    meta: AssistantTemplateMeta
    files_collection_id: Optional[str] = None
    streams: list[AssistantStreamConfig | AssistantStreamPipelineDef]
