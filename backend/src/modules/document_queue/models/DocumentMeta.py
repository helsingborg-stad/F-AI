from pydantic import BaseModel


class DocumentMeta(BaseModel):
    space_id: str
    document_id: str
    embedding_model: str
    source_name: str
