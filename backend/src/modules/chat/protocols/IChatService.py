from typing import Protocol, AsyncGenerator

from src.modules.chat.models.ChatEvent import ChatEvent


class IChatService(Protocol):
    def start_new_chat(self, as_uid: str, assistant_id: str, message: str) -> AsyncGenerator[ChatEvent, None]:
        ...

    def continue_chat(self, as_uid: str, conversation_id: str, message: str) -> AsyncGenerator[ChatEvent, None]:
        ...
