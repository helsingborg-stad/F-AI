import asyncio
import base64
from datetime import datetime
from random import random
from typing import Protocol, AsyncGenerator

from langstream import Stream, StreamOutput
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage
from pydantic import BaseModel


class ILLMProtocol(Protocol):
    def run(self, input_message: str) -> AsyncGenerator[StreamOutput[str], str]:
        """
        Takes an input message and returns an async stream resolving to the response from the LLM.

        :param input_message: The input message, as a string.
        :type input_message: str

        :return: The resulting `Stream[str, str]` object.
        :rtype: Stream[str, str]

        """
        ...


class OpenAILLM(ILLMProtocol):

    def __init__(self, template: str):
        self.template = template

    def run(self, input_message: str) -> AsyncGenerator[StreamOutput[str], str]:
        llm_stream: Stream[str, str] = OpenAIChatStream[str, OpenAIChatDelta](
            "RecipeStream",
            lambda user_question: [
                OpenAIChatMessage(
                    role="system",
                    content=self.template
                ),
                OpenAIChatMessage(
                    role="user",
                    content=f"{user_question}",
                ),
            ],
            model="gpt-4",
            temperature=0,
        ).map(lambda delta: delta.content)

        return llm_stream(input_message)


class ParrotLLM(ILLMProtocol):

    @staticmethod
    async def to_generator(input_message: str):
        import re
        parts = re.findall(r'\S+\s*', input_message)
        for part in parts:
            yield part
            await asyncio.sleep(random() * 1)

    def run(self, input_message: str) -> AsyncGenerator[StreamOutput[str], str]:
        stream = Stream[str, str](
            "ParrotStream",
            self.to_generator
        )
        return stream(input_message)


class LLMMessage(BaseModel):
    type: str
    date: datetime
    source: str | None = None
    content: str | None = None


class ISerializer(Protocol):
    def serialize(self, input_data: LLMMessage) -> str:
        """

        """
        ...


class SSESerializer(ISerializer):
    def serialize(self, input_data: LLMMessage) -> str:
        output_data: str = input_data.copy(update={"type": None}).model_dump_json(exclude_none=True)

        # encode output_data to base64 preserving utf-8
        base64string = base64.b64encode(output_data.encode("utf-8")).decode("utf-8")

        return f"event: {input_data.type}\ndata: {base64string}\n\n"


class JSONSerializer(ISerializer):
    def serialize(self, input_data: LLMMessage) -> str:
        return input_data.model_dump_json(exclude_none=True)


if __name__ == "__main__":
    async def main():
        llm = ParrotLLM()
        # llm = OpenAILLM("Always answer in Swedish.")
        serializer = SSESerializer()
        # serializer = JSONSerializer()

        async for output in llm.run("Hello how are you doing?"):
            if isinstance(output.data, str):
                print(serializer.serialize(LLMMessage(
                    type="message",
                    date=datetime.now(),
                    source=output.stream,
                    content=output.data
                )))

        print(serializer.serialize(LLMMessage(
            type="message_end",
            date=datetime.now()
        )))


    asyncio.run(main())
