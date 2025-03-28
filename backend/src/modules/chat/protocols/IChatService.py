from typing import Protocol, AsyncGenerator

from src.modules.chat.models.MessageDelta import MessageDelta


class IChatService(Protocol):
    def start_new_chat(self, assistant_id: str, message: str) -> AsyncGenerator[MessageDelta, None]:
        ...

    def continue_chat(self, conversation_id: str, message: str) -> AsyncGenerator[MessageDelta, None]:
        ...
