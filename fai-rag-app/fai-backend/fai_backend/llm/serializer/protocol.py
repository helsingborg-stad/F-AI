from typing import Protocol

from fai_backend.llm.models import LLMMessage


class ISerializer(Protocol):
    def serialize(self, input_data: LLMMessage) -> str:
        """

        """
        ...
