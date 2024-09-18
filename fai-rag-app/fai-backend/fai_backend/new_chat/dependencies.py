from typing import List

from fai_backend.assistant.models import ClientChatState


class ChatHistoryService:
    def get_chat_history(self) -> List[ClientChatState]:
        return [self.create_client_chat_state()]

    @staticmethod
    def create_client_chat_state() -> ClientChatState:
        return ClientChatState(id='123',
                               title='My title',
                               timestamp='20240101',
                               history=[])


def get_chat_history_service() -> ChatHistoryService:
    return ChatHistoryService()
