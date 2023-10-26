

from pydantic import BaseModel


from typing import List, Optional


class InputFeedback(BaseModel):
    comment: Optional[str] = None
    rating: str

class InputMessage(BaseModel):
    user: str
    content: str

class InputConversation(BaseModel):
    messages: List[InputMessage]

