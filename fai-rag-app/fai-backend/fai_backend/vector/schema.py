from pydantic import BaseModel


class VectorData(BaseModel):
    documents: list[str]


class VectorizeFilesModel(BaseModel):
    directory_path: str
