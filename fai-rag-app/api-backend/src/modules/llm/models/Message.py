from pydantic import BaseModel

from src.modules.llm.models import ToolCall


class Message(BaseModel):
    role: str
    content: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[ToolCall] | None = None
