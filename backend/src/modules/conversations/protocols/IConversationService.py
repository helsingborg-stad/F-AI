from typing import Protocol

from src.modules.conversations.models.Conversation import Conversation


class IConversationService(Protocol):
    async def create_conversation(self, as_uid: str, assistant_id: str) -> str:
        ...

    async def get_conversation(self, as_uid: str, conversation_id: str) -> Conversation | None:
        ...

    async def get_conversations(self, as_uid: str) -> list[Conversation]:
        ...

    async def add_message_to_conversation(self, as_uid: str, conversation_id: str, timestamp: str, role: str,
                                          message: str) -> bool:
        ...

    async def add_to_conversation_last_message(
            self, as_uid: str,
            conversation_id: str,
            timestamp: str,
            role: str,
            additional_message: str
    ) -> bool:
        ...

    async def set_conversation_title(self, as_uid: str, conversation_id: str, title: str) -> bool:
        ...

    async def delete_conversation(self, as_uid: str, conversation_id: str):
        ...
