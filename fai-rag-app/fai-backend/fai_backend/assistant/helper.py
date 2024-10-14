from typing import Callable, Any

from langstream import Stream

from fai_backend.assistant.models import AssistantStreamMessage, AssistantStreamInsert, AssistantContext
from fai_backend.assistant.protocol import IAssistantContextStore, IAssistantMessageInsert


def messages_expander_stream(
        messages: list[AssistantStreamMessage | AssistantStreamInsert],
        context_store: IAssistantContextStore,
        get_insert: Callable[[str], IAssistantMessageInsert]
) -> Stream[Any, list[AssistantStreamMessage]]:
    async def _expand_message(message: AssistantStreamMessage | AssistantStreamInsert) -> list[AssistantStreamMessage]:
        if isinstance(message, AssistantStreamMessage):
            return [AssistantStreamMessage(
                **message.model_dump(exclude={'should_format'}),  # TODO: eww
                should_format=True
            )]
        return await get_insert(message.insert).get_messages(context_store)

    async def _parse_messages(_):
        lists = [await _expand_message(m) for m in messages]
        yield [m for sublist in lists for m in sublist]

    return Stream('expander', _parse_messages)


def get_message_content(message: AssistantStreamMessage, context: AssistantContext):
    if message.should_format:
        return message.content.format(**context.dict())
    return message.content
