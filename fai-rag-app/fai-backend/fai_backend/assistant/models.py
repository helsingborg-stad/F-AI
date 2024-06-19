from datetime import datetime
from typing import Optional, Dict, List, Any, Literal, Union

from pydantic import BaseModel


class LLMStreamMessage(BaseModel):
    role: Literal["system", "user", "assistant", "function"]
    content: str


class LLMStreamSettings(BaseModel):
    model: str
    temperature: Optional[float] = 0
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[Union[Literal["none", "auto"], Dict[str, Any]]] = None


class LLMStreamDef(BaseModel):
    name: str
    settings: LLMStreamSettings
    messages: Optional[List[LLMStreamMessage]] = None


class AssistantTemplate(BaseModel):
    id: str
    name: str
    files_collection_id: Optional[str] = None
    description: Optional[str] = None
    sample_questions: list[str] = []
    streams: List[LLMStreamDef]


class LLMClientChatMessage(BaseModel):
    date: datetime
    source: str | None = None
    content: str | None = None
