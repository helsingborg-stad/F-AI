from pydantic import BaseModel


class CollectionFile(BaseModel):
    name: str
