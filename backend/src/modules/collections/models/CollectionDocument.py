from typing import Literal

from pydantic import BaseModel


class CollectionDocument(BaseModel):
    id: str
    name: str
    type: str
    state: Literal['queued', 'processing', 'ready', 'error']
