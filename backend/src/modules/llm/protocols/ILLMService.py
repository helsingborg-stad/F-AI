from collections.abc import AsyncGenerator
from typing import Protocol

from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Feature import Feature
from src.modules.llm.models.Message import Message


class ILLMService(Protocol):
    def run(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            enabled_features: list[Feature],
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> AsyncGenerator[Delta, None]:
        ...

    async def run_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            response_schema: dict[str, object] | None = None,
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> Message:
        ...
