from typing import Any

from pydantic import BaseModel


class AssistantInfo(BaseModel):
    id: str
    model: str
    meta: dict[str, Any]
