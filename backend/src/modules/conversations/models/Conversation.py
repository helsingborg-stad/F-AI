from pydantic import BaseModel

from src.modules.conversations.models.Message import Message


class Conversation(BaseModel):
    id: str
    assistant_id: str
    title: str
    messages: list[Message]
