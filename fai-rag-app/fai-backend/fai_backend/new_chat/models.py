from pydantic import BaseModel

from fai_backend.assistant.models import LLMClientChatMessage


class ClientChatState(BaseModel):
    user: str
    chat_id: str
    timestamp: str
    title: str
    delete_label: str = "Delete"  # TODO: fix hack for allowing something to show up in list to click on.
    rename_label: str = "Rename"  # TODO: fix hack for allowing something to show up in list to click on.
    history: list[LLMClientChatMessage]
    max_tokens: int
    allow_inline_files: bool


class ChatHistoryEditPayload(BaseModel):
    chat_id: str
    title: str
