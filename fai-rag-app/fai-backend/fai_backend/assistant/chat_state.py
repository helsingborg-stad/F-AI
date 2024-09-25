from typing import List

from fai_backend.assistant.models import AssistantChatHistoryModel, ClientChatState, LLMClientChatMessage
from fai_backend.repositories import ChatHistoryRepository, chat_history_repo
from fai_backend.repository.query.component import AttributeAssignment


class ChatStateService:
    def __init__(self, history_repo: ChatHistoryRepository):
        self.history_repo = history_repo

    async def get_states(self, user: str) -> List[ClientChatState]:
        results = await self.history_repo.list(query=AttributeAssignment('user', user))
        return [ChatStateService.assistant_chat_history_model_to_chat_state(r) for r in results if len(r.history) > 0]

    async def get_state(self, chat_id: str) -> ClientChatState:
        history = await self.history_repo.get(chat_id)
        return ChatStateService.assistant_chat_history_model_to_chat_state(history)

    @staticmethod
    def assistant_chat_history_model_to_chat_state(
            chat_history_model: AssistantChatHistoryModel
    ) -> ClientChatState:
        return ClientChatState(
            user=chat_history_model.user,
            chat_id=str(chat_history_model.id),
            timestamp=chat_history_model.history[0].timestamp,
            title=f'{chat_history_model.history[0].content[:30]}...',  # TODO: replace with pre-generated AI title
            history=[LLMClientChatMessage(
                timestamp=m.timestamp,
                source=m.role,
                content=m.content
            ) for m in chat_history_model.history]
        )


def get_chat_state_service():
    return ChatStateService(chat_history_repo)
