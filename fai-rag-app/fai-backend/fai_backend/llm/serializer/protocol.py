from typing import Protocol

from pydantic import BaseModel


class ISerializer(Protocol):
    def serialize(self, input_data: BaseModel) -> str:
        """

        """
        ...
