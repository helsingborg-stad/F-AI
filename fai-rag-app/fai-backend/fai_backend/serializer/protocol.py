from typing import Protocol, Type, TypeVar

from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class ISerializer(Protocol[T]):
    def serialize(self, input_data: T) -> str:
        """

        """
        ...

    def deserialize(self, input_data: str, type_class: Type[BaseModel]) -> T:
        """

        """
        ...
