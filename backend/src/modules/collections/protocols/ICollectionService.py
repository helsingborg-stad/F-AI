from typing import Protocol, Literal

from src.modules.collections.models.CollectionMetadata import CollectionMetadata
from src.modules.collections.models.CollectionQueryResult import CollectionQueryResult


class ICollectionService(Protocol):
    async def create_collection(self, label: str, embedding_model: str) -> str:
        ...

    async def get_collection(self, collection_id: str) -> CollectionMetadata | None:
        ...

    async def get_collections(self) -> list[CollectionMetadata]:
        ...

    async def set_collection_label(self, collection_id: str, label: str) -> bool:
        ...

    async def set_collection_documents(self, collection_id: str, paths_and_urls: list[str]) -> bool:
        ...

    async def update_collection_document(self, collection_id: str, document_id: str,
                                         state: Literal['queued', 'processing', 'ready', 'error']) -> bool:
        ...

    async def query_collection(self, collection_id: str, query: str, max_results: int) -> list[CollectionQueryResult]:
        ...

    async def delete_collection(self, collection_id: str):
        ...
