from pydantic import BaseModel


class MessageDelta(BaseModel):
    conversation_id: str
    source: str
    message: str
