from pydantic import BaseModel

from fai_llm.serializer.protocol import ISerializer


class JSONSerializer(ISerializer):
    def serialize(self, input_data: BaseModel) -> str:
        return input_data.model_dump_json(exclude_none=True)
