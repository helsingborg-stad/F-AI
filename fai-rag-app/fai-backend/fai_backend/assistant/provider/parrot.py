import asyncio
import random
from typing import Callable, Any

from langstream import Stream

from fai_backend.assistant.helper import messages_expander_stream, get_message_content
from fai_backend.assistant.models import AssistantStreamMessage, AssistantStreamInsert
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantContextStore, IAssistantMessageInsert


class ParrotLLMProvider(IAssistantLLMProvider):
    def __init__(self):
        pass

    async def create_llm_stream(
            self,
            messages: list[AssistantStreamMessage | AssistantStreamInsert],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert],
    ) -> Stream[Any, Any]:
        async def squawk_back(last_message: AssistantStreamMessage):
            parts = get_message_content(last_message, context_store.get_mutable()).split(sep=' ')
            r = random.Random()
            for part in parts:
                if r.random() < 0.5:
                    yield r' _**squawk**_ '
                yield part + ' '
                await asyncio.sleep(r.random())

        parrot_stream = Stream('parrot', lambda in_data: squawk_back(in_data[0][-1]))

        return messages_expander_stream(messages, context_store, get_insert).and_then(parrot_stream)
