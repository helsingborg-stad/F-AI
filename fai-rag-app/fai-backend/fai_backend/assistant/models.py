from typing import Optional, Dict, List, Any, Literal, Union

from pydantic import BaseModel


class LLMStreamMessage(BaseModel):
    role: str
    content: str


class LLMStreamSettings(BaseModel):
    model: str
    temperature: Optional[float] = 0
    functions: Optional[List[Dict[str, Any]]] = None
    function_call: Optional[Union[Literal["none", "auto"], Dict[str, Any]]] = None


class LLMStream(BaseModel):
    name: str
    settings: LLMStreamSettings
    messages: Optional[List[LLMStreamMessage]] = None


class AssistantTemplate(BaseModel):
    name: str
    files_collection_id: Optional[str] = None
    streams: List[LLMStream]
