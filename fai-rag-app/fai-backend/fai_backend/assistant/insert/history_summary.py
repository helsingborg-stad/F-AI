from langstream import join_final_output
from langstream.contrib import OpenAIChatStream, OpenAIChatDelta, OpenAIChatMessage

from fai_backend.assistant.helper import get_message_content
from fai_backend.assistant.models import AssistantStreamMessage
from fai_backend.assistant.protocol import IAssistantMessageInsert, IAssistantContextStore


class AssistantHistorySummaryInsert(IAssistantMessageInsert):
    async def get_messages(self, context_store: IAssistantContextStore) -> list[AssistantStreamMessage]:
        context = context_store.get_mutable()

        if len(context.history) == 0:
            return []

        summarize_stream = OpenAIChatStream[str, OpenAIChatDelta](
            "openai",
            lambda in_data: [
                                OpenAIChatMessage(
                                    content=get_message_content(message, context),
                                    role=message.role
                                ) for message in context.history
                            ] + [OpenAIChatMessage(
                role='user',
                content='summarize what has been said so far.'
            )],
            model='gpt-3.5-turbo',
            temperature=0,
        ).map(lambda delta: delta.content)

        summary = await join_final_output(summarize_stream(None))
        return [AssistantStreamMessage(
            timestamp=context.history[0].timestamp,
            role='assistant',
            content=summary,
        )] + context.history[-3:]
