from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage

from fai_backend.llm.protocol import ILLMStreamProtocol
from fai_backend.llm.models import LLMDataPacket


class OpenAILLM(ILLMStreamProtocol):

    def __init__(self, template: str):
        self.template = template

    async def create(self) -> Stream[str, LLMDataPacket]:
        return OpenAIChatStream[str, OpenAIChatDelta](
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
        ).map(lambda delta: LLMDataPacket(content=delta.content, user_friendly=True))
