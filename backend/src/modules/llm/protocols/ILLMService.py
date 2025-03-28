from collections.abc import AsyncGenerator
from typing import Protocol

from src.modules.llm.models.Message import Message
from src.modules.llm.models.Delta import Delta


class ILLMService(Protocol):
    def stream_llm(
            self,
            model: str,
            messages: list[Message],
            max_tokens: int = 0,
            temperature: float = 0.0,
            api_key: str = ''
    ) -> AsyncGenerator[Delta, None]:
        ...

    async def run_llm(
            self,
            model: str,
            messages: list[Message],
            max_tokens: int = 0,
            temperature: float = 0.0,
            api_key: str = ''
    ) -> Message:
        ...
