from pydantic import BaseModel


class CollectionQueryResult(BaseModel):
    content: str
    source: str
    page_number: int | None
