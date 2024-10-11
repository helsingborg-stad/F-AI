from typing import Optional

from fai_backend.collection.service import CollectionService
from fai_backend.vector.embedding import EmbeddingFnFactory
from fai_backend.vector.interface import IVector
from fai_backend.vector.types import OneOrMany


class VectorService:
    vector_db: IVector
    collection_meta_service: CollectionService

    def __init__(self, vector_db: IVector, collection_meta_service: CollectionService):
        self.vector_db = vector_db
        self.collection_meta_service = collection_meta_service

    async def create_collection(self, collection_name: str, embedding_model: str | None = None):
        await self.vector_db.create_collection(collection_name,
                                               EmbeddingFnFactory.create(embedding_model))

    async def delete_collection(self, collection_name: str):
        await self.vector_db.delete_collection(collection_name)

    async def add_to_collection(
            self,
            collection_name: str,
            ids: OneOrMany[str],
            documents: Optional[OneOrMany[str]],
            embedding_model: str | None = None
    ) -> None:
        await self.vector_db.add(
            collection_name=collection_name,
            ids=ids,
            documents=documents,
            embedding_function=EmbeddingFnFactory.create(embedding_model)
        )

    async def add_documents_without_id_to_empty_collection(
            self,
            collection_name: str,
            documents: list[str],
            embedding_model: str | None = None
    ) -> None:
        """
        Add documents to a collection without specifying ID's

        The collection should be empty before calling this method to avoid ID conflicts.
        """
        ids = [str(i) for i in range(len(documents))]
        await self.add_to_collection(
            collection_name=collection_name,
            ids=ids,
            documents=documents,
            embedding_model=embedding_model
        )

    async def query_from_collection(
            self,
            collection_name: str,
            query_texts: Optional[OneOrMany[str]] = None,
            n_results: int = 10,
    ):
        collection_meta = await self.collection_meta_service.get_collection_metadata(collection_name)
        embedding_model = collection_meta[0].embedding_model if collection_meta and collection_meta[0] else None

        return await self.vector_db.query(
            collection_name=collection_name,
            query_texts=query_texts,
            n_results=n_results,
            embedding_function=EmbeddingFnFactory.create(embedding_model),
        )

    async def list_collections(self):
        return await self.vector_db.list_collections()
