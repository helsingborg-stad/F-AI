from pydantic import BaseModel


class Message(BaseModel):
    timestamp: str
    role: str
    content: str
