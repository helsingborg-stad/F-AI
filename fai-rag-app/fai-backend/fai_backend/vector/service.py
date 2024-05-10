from typing import Optional

from fai_backend.vector.interface import IVector
from fai_backend.vector.types import OneOrMany


class VectorService:
    vector_db: IVector

    def __init__(self, vector_db):
        self.vector_db = vector_db

    async def create_collection(self, collection_name: str):
        await self.vector_db.create_collection(collection_name)

    async def delete_collection(self, collection_name: str):
        await self.vector_db.delete_collection(collection_name)

    async def add_to_collection(
            self,
            collection_name: str,
            ids: OneOrMany[str],
            documents: Optional[OneOrMany[str]],
    ) -> None:
        await self.vector_db.add(
            collection_name=collection_name,
            ids=ids,
            documents=documents,
        )

    async def add_documents_without_id_to_empty_collection(
            self,
            collection_name: str,
            documents: list[str]
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
        )

    async def query_from_collection(
            self,
            collection_name: str,
            query_texts: Optional[OneOrMany[str]] = None,
            n_results: int = 10,
    ):
        return await self.vector_db.query(
            collection_name=collection_name,
            query_texts=query_texts,
            n_results=n_results,
        )

    async def list_collections(self):
        return await self.vector_db.list_collections()
