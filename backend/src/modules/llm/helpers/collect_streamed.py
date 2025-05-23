from typing import AsyncGenerator, Callable

from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message
from src.modules.llm.models.ToolCall import ToolCall


async def collect_streamed(
        stream_llm_func: Callable[
            [str, str, list[Message], dict[str, object] | None, dict], AsyncGenerator[Delta, None]],
        model: str,
        api_key: str,
        messages: list[Message],
        response_schema: dict[str, object] | None = None,
        extra_params: dict[str, float | int | bool | str] | None = None
):
    role: str | None = None
    content: str | None = None
    tool_calls: list[ToolCall] | None = None

    async for output in stream_llm_func(model, api_key, messages, response_schema, extra_params):
        role = output.role if output.role else role
        content = (content or '') + output.content if output.content else content
        tool_calls = output.tool_calls if output.tool_calls else tool_calls

    return Message(
        role=role,
        content=content,
        tool_call_id=None,
        tool_calls=tool_calls
    )
