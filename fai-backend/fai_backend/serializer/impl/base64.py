import base64

from pydantic import BaseModel

from fai_backend.serializer.protocol import ISerializer


class Base64Serializer(ISerializer):
    def serialize(self, input_data: BaseModel) -> str:
        output_data: str = input_data.model_dump_json(exclude_none=True)
        return base64.b64encode(output_data.encode("utf-8")).decode("utf-8")
