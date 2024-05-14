from fai_backend.llm.models import LLMMessage
from fai_backend.llm.serializer.protocol import ISerializer


class JSONSerializer(ISerializer):
    def serialize(self, input_data: LLMMessage) -> str:
        return input_data.model_dump_json(exclude_none=True)
