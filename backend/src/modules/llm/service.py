from collections.abc import AsyncGenerator

from src.modules.llm.models.Message import Message
from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.ToolCall import ToolCall
from src.modules.llm.protocols.ILLMService import ILLMService
from src.modules.llm.runner import OpenAIRunner


class LLMService(ILLMService):
    async def stream(self, model: str, messages: list[Message]) -> AsyncGenerator[Delta, None]:
        runner = OpenAIRunner(
            model=model,
            messages=messages,
            temperature=1
        )
        async for output in runner.run():
            yield output

    async def run(self, model: str, messages: list[Message]) -> Message:
        role: str | None = None
        content: str | None = None
        tool_calls: list[ToolCall] | None = None

        async for output in self.stream(model, messages):
            role = output.role if output.role else role
            content = (content or '') + output.content if output.content else content
            tool_calls = output.tool_calls if output.tool_calls else tool_calls

        return Message(
            role=role,
            content=content,
            tool_call_id=None,
            tool_calls=tool_calls
        )
