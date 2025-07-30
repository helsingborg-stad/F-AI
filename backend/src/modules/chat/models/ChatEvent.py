from typing import Literal, Union

from pydantic import BaseModel


class ChatErrorEvent(BaseModel):
    event: Literal['error'] = 'error'
    message: str


class ChatConversationIdEvent(BaseModel):
    event: Literal['conversation_id'] = 'conversation_id'
    conversation_id: str


class ChatMessageEvent(BaseModel):
    event: Literal['message'] = 'message'
    source: str
    message: str | None = None
    reasoning: str | None = None


ChatEvent = Union[ChatErrorEvent, ChatConversationIdEvent, ChatMessageEvent]
