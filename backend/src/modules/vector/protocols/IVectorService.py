from typing import Protocol

from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.models.VectorSpace import VectorSpace


class IVectorService(Protocol):
    async def create_vector_space(self, space: str, embedding_model: str):
        ...

    async def add_documents_to_vector_space(self, space: str, embedding_model: str, documents: list[VectorDocument]):
        ...

    async def delete_vector_space(self, space: str):
        ...

    async def get_vector_spaces(self) -> list[VectorSpace]:
        ...

    async def query_vector_space(
            self,
            space: str,
            embedding_model: str,
            query: str,
            max_results: int
    ) -> list[VectorDocument]:
        ...
