from collections.abc import AsyncGenerator
from typing import Protocol

from src.modules.llm.models.Message import Message
from src.modules.llm.models.Delta import Delta


class ILLMService(Protocol):
    async def stream(self, model: str, messages: list[Message]) -> AsyncGenerator[Delta, None]:
        ...

    async def run(self, model: str, messages: list[Message]) -> Message:
        ...
