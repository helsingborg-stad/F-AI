from fai_llm.assistant.models import AssistantStreamMessage
from fai_llm.assistant.protocol import IAssistantMessageInsert, IAssistantContextStore


class AssistantHistoryInsert(IAssistantMessageInsert):
    async def get_messages(self, context_store: IAssistantContextStore) -> list[AssistantStreamMessage]:
        context = context_store.get_mutable()
        return context.history
