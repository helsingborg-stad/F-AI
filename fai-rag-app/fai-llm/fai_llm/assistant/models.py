from datetime import datetime
from typing import Optional, Any, Literal

from pydantic import BaseModel


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


class AssistantTemplate(BaseModel, extra='ignore'):
    files_collection_id: Optional[str] = None
    streams: list[AssistantStreamConfig | AssistantStreamPipelineDef]


class AssistantContext(BaseModel):
    query: str = ""
    files_collection_id: Optional[str] = None
    previous_stream_output: Optional[str] = None
    history: list[AssistantStreamMessage] = []
    rag_output: Optional[str] = None
