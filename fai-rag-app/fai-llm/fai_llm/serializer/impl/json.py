from typing import Type

from pydantic import BaseModel

from fai_llm.serializer.protocol import ISerializer, T


class JSONSerializer(ISerializer[T]):
    def serialize(self, input_data: BaseModel) -> str:
        return input_data.model_dump_json(exclude_none=True)

    def deserialize(self, input_data: str, type_class: Type[BaseModel]) -> T:
        return type_class.model_validate_json(input_data)
