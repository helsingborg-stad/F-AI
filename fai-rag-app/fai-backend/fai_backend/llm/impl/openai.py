from typing import AsyncGenerator

from langstream import StreamOutput, Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage

from fai_backend.llm.protocol import ILLMProtocol


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
