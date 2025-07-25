from typing import Protocol, AsyncGenerator

from src.modules.chat.models.ChatEvent import ChatEvent
from src.modules.ai.completions.models.Feature import Feature


class IChatService(Protocol):
    def start_new_chat(self, as_uid: str, assistant_id: str, message: str, enabled_features: list[Feature]) -> \
    AsyncGenerator[
        ChatEvent, None]:
        ...

    def continue_chat(self, as_uid: str, conversation_id: str, message: str, enabled_features: list[Feature]) -> \
    AsyncGenerator[
        ChatEvent, None]:
        ...
