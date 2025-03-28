from collections.abc import AsyncGenerator

from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message
from src.modules.llm.models.ToolCall import ToolCall
from src.modules.llm.protocols.ILLMService import ILLMService
from src.modules.llm.runner import OpenAIRunner


class OpenAILLMService(ILLMService):
    async def stream_llm(
            self,
            model: str,
            messages: list[Message],
            max_tokens: int = 0,
            temperature: float = 0.0,
            api_key: str = '',
    ) -> AsyncGenerator[Delta, None]:
        runner = OpenAIRunner(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            api_key=api_key,
        )
        async for output in runner.run():
            yield output

    async def run_llm(
            self,
            model: str,
            messages: list[Message],
            max_tokens: int = 0,
            temperature: float = 0.0,
            api_key: str = ''
    ) -> Message:
        role: str | None = None
        content: str | None = None
        tool_calls: list[ToolCall] | None = None

        async for output in self.stream_llm(model, messages, max_tokens, temperature, api_key):
            role = output.role if output.role else role
            content = (content or '') + output.content if output.content else content
            tool_calls = output.tool_calls if output.tool_calls else tool_calls

        return Message(
            role=role,
            content=content,
            tool_call_id=None,
            tool_calls=tool_calls
        )
