from pydantic import BaseModel

from src.modules.collections.models.CollectionFile import CollectionFile


class CollectionMetadata(BaseModel):
    id: str
    label: str
    embedding_model: str
    files: list[CollectionFile]
    urls: list[str]
