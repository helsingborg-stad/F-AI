import base64

from fai_backend.llm.models import LLMMessage
from fai_backend.llm.serializer.protocol import ISerializer


class SSESerializer(ISerializer):
    def serialize(self, input_data: LLMMessage) -> str:
        output_data: str = input_data.copy(update={"type": None}).model_dump_json(exclude_none=True)
        base64string = base64.b64encode(output_data.encode("utf-8")).decode("utf-8")
        return f"event: {input_data.type}\ndata: {base64string}\n\n"
