from typing import List

from fai_backend.assistant.models import (AssistantChatHistoryModel, AssistantStreamMessage, LLMClientChatMessage)
from fai_backend.new_chat.models import ClientChatState
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

    async def delete_state(self, chat_id: str) -> None:
        await self.history_repo.delete(chat_id)

    async def update_state(self, chat_id: str, new_state: ClientChatState) -> None:
        new_history = await self.chat_state_to_assistant_chat_history_model(new_state)
        ignore_keys = ['id', 'timestamp']

        await self.history_repo.update(chat_id, {key: new_history.model_dump()[key]
                                                 for key in filter(lambda key: key not in ignore_keys,
                                                                   new_history.model_dump().keys())})

    async def chat_state_to_assistant_chat_history_model(self,
                                                         chat_state: ClientChatState) -> AssistantChatHistoryModel:
        supplementary_history = await self.history_repo.get(chat_state.chat_id)
        return AssistantChatHistoryModel(user=chat_state.user,
                                         title=chat_state.title,
                                         assistant=supplementary_history.assistant,
                                         history=[AssistantStreamMessage(
                                             timestamp=a.timestamp,
                                             role=a.source,
                                             content=a.content) for a in chat_state.history])

    @staticmethod
    def assistant_chat_history_model_to_chat_state(chat_history_model: AssistantChatHistoryModel) -> ClientChatState:
        def convert_message(m: AssistantStreamMessage) -> LLMClientChatMessage:
            return LLMClientChatMessage(timestamp=m.timestamp, source=m.role, content=m.content)

        title = chat_history_model.title
        default_title = title if title else chat_history_model.history[0].content[
                                            :30] + '...'  # TODO: replace title with pre-generated AI title

        return ClientChatState(user=chat_history_model.user,
                               chat_id=str(chat_history_model.id),
                               timestamp=chat_history_model.history[0].timestamp,
                               title=default_title,
                               history=[convert_message(message) for message in chat_history_model.history])
