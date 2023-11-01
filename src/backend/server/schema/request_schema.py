from pydantic import BaseModel, Field


from typing import List


class InputFeedback(BaseModel):
    comment: str = Field(default=None)
    rating: str


class InputMessage(BaseModel):
    user: str
    content: str


class InputConversation(BaseModel):
    messages: List[InputMessage]
