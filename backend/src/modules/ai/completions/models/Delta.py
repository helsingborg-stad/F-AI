from pydantic import BaseModel


class Delta(BaseModel):
    role: str
    content: str | None = None
    reasoning_content: str | None = None
    tool_call_id: str | None = None
    tool_calls: list[dict] | None = None
    context_message_override: str | None = None
