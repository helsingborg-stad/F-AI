from typing import AsyncGenerator

from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message
from src.modules.llm.models.ToolCall import ToolCall


async def collect_streamed(generator: AsyncGenerator[Delta, None]):
    role: str | None = None
    content: str | None = None
    tool_calls: list[ToolCall] | None = None

    async for output in generator:
        role = output.role if output.role else role
        content = (content or '') + output.content if output.content else content
        tool_calls = output.tool_calls if output.tool_calls else tool_calls

    return Message(
        role=role,
        content=content,
        tool_call_id=None,
        tool_calls=tool_calls
    )
