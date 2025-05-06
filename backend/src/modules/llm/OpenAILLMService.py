from collections.abc import AsyncGenerator

from src.modules.llm.helpers.collect_streamed import collect_streamed
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message
from src.modules.llm.openai_runner import OpenAIRunner
from src.modules.llm.protocols.ILLMService import ILLMService


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
        return await collect_streamed(
            stream_llm_func=self.stream_llm,
            model=model,
            api_key=api_key,
            messages=messages,
            extra_params=extra_params
        )
