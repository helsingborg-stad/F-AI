from pydantic import BaseModel


class CollectionDocuments(BaseModel):
    files: list[str]
    urls: list[str]
