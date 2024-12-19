from beanie import Document
from pydantic import BaseModel


class CollectionFile(BaseModel):
    id: str
    name: str
    upload_timestamp: str
    byte_size: int


class CollectionMetadataModel(Document):
    collection_id: str
    label: str = ''
    description: str = ''
    embedding_model: str | None = ''
    urls: list[str] | None = None
    files: list[CollectionFile] = []

    class Settings:
        name = 'collections'
        use_state_management = True
