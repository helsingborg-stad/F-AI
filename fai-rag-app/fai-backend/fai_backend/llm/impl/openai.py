from typing import Iterable, Any

from langstream import Stream
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage

from fai_backend.chat.stream import create_chat_prompt
from fai_backend.chat.template import PromptTemplate
from fai_backend.llm.protocol import ILLMStreamProtocol
from fai_backend.llm.models import LLMDataPacket


class OpenAILLM(ILLMStreamProtocol):

    def __init__(self, template: PromptTemplate):
        self.template = template

    async def create(self) -> Stream[str, LLMDataPacket]:
        def messages(in_data: Any) -> Iterable[OpenAIChatMessage]:
            prompt = create_chat_prompt({
                "name": self.template.name,
                "messages": self.template.messages,
                "settings": self.template.settings,
            })
            prompt.format_prompt(self.template.input_map_fn(in_data))
            return prompt.to_messages()

        return OpenAIChatStream[str, OpenAIChatDelta](
            "RecipeStream",
            messages,
            model="gpt-4",
            temperature=0,
        ).map(lambda delta: LLMDataPacket(content=delta.content, user_friendly=True))
