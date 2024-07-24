import base64
import json
from typing import Any, Type

from pydantic import BaseModel

from fai_llm.serializer.protocol import ISerializer, T


class Base64Serializer(ISerializer[T]):
    def serialize(self, input_data: T) -> str:
        output_data: str = input_data.model_dump_json(exclude_none=True)
        return base64.b64encode(output_data.encode("utf-8")).decode("utf-8")

    def deserialize(self, input_data: str, type_class: Type[BaseModel]) -> T:
        decoded = base64.b64decode(input_data.encode("utf-8")).decode("utf-8")
        return type_class.model_validate_json(decoded)
