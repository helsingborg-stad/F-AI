from datetime import datetime

from pydantic import BaseModel


class LLMMessage(BaseModel):
    type: str
    date: datetime
    source: str | None = None
    content: str | None = None
