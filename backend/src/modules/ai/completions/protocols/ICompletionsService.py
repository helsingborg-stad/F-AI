from collections.abc import AsyncGenerator
from typing import Protocol

from src.modules.ai.completions.models.Delta import Delta
from src.modules.ai.completions.models.Feature import Feature
from src.modules.ai.completions.models.Message import Message


class ICompletionsService(Protocol):
    def run_completions(
            self,
            messages: list[Message],
            enabled_features: list[Feature],
            extra_params: dict | None = None
    ) -> AsyncGenerator[Delta, None]:
        ...
