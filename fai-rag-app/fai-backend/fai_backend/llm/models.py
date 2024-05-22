import dataclasses
from datetime import datetime

from pydantic import BaseModel


class LLMMessage(BaseModel):
    date: datetime
    source: str | None = None
    content: str | None = None


@dataclasses.dataclass
class LLMDataPacket:
    content: str
    user_friendly: bool = False
