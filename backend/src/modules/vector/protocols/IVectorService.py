from typing import Protocol

from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.models.VectorSpace import VectorSpace


class IVectorService(Protocol):
    async def create(self, space: str, embedding_model: str):
        ...

    async def add_to(self, space: str, embedding_model: str, documents: list[VectorDocument]):
        ...

    async def delete(self, space: str):
        ...

    async def list_spaces(self) -> list[VectorSpace]:
        ...

    async def query(self, space: str, embedding_model: str, query: str, max_results: int) -> list[VectorDocument]:
        ...
