from collections.abc import AsyncGenerator
from typing import Protocol

from src.modules.llm.models.Message import Message
from src.modules.llm.models.Delta import Delta


class ILLMService(Protocol):
    def stream_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> AsyncGenerator[Delta, None]:
        ...

    async def run_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> Message:
        ...
