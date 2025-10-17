from typing import Literal

from pydantic import BaseModel


class DocumentStateUpdate(BaseModel):
    space_id: str
    document_id: str
    status: Literal['processing', 'ready', 'error']
