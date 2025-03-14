from typing import Any

from pydantic import BaseModel


class VectorDocument(BaseModel):
    id: str
    content: str
    metadata: dict[str, Any] | None
