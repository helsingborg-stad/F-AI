from pydantic import BaseModel

from src.modules.llm.models.ToolCall import ToolCall


class Delta(BaseModel):
    role: str
    content: str | None = None
    tool_calls: list[ToolCall] | None = None
