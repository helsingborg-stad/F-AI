from typing import Literal

from pydantic import BaseModel


class ChatEvent(BaseModel):
    event: Literal['error', 'conversation_id', 'message', 'reasoning']
    conversation_id: str | None = None
    source: str | None = None
    message: str | None = None
    reasoning: str | None = None
