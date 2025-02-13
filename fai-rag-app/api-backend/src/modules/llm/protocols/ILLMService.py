from collections.abc import AsyncGenerator
from typing import Protocol

from src.modules.llm.models import Message, Delta


class ILLMService(Protocol):
    async def stream(self, model: str, messages: list[Message]) -> AsyncGenerator[Delta, None]:
        ...

    async def run(self, model: str, messages: list[Message]) -> Message:
        ...
