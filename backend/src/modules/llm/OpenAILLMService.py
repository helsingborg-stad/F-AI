from collections.abc import AsyncGenerator

from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message
from src.modules.llm.models.ToolCall import ToolCall
from src.modules.llm.protocols.ILLMService import ILLMService
from src.modules.llm.openai_runner import OpenAIRunner


class OpenAILLMService(ILLMService):
    async def stream_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> AsyncGenerator[Delta, None]:
        [_, model_name] = parse_model_key(model)
        runner = OpenAIRunner(
            model=model_name,
            messages=messages,
            api_key=api_key,
            max_tokens=extra_params.get('max_tokens', None),
            temperature=extra_params.get('temperature', None),
        )
        async for output in runner.run():
            yield output

    async def run_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> Message:
        role: str | None = None
        content: str | None = None
        tool_calls: list[ToolCall] | None = None

        async for output in self.stream_llm(
                api_key=api_key,
                model=model,
                messages=messages,
                extra_params=extra_params
        ):
            role = output.role if output.role else role
            content = (content or '') + output.content if output.content else content
            tool_calls = output.tool_calls if output.tool_calls else tool_calls

        return Message(
            role=role,
            content=content,
            tool_call_id=None,
            tool_calls=tool_calls
        )
