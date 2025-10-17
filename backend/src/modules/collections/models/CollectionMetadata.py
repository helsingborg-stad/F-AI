from pydantic import BaseModel

from src.modules.collections.models.CollectionDocument import CollectionDocument


class CollectionMetadata(BaseModel):
    id: str
    label: str
    embedding_model: str
    documents: list[CollectionDocument]
