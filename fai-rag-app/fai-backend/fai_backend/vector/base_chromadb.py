from typing import Union, Optional, Mapping, Set
import numpy as np
from chromadb import ClientAPI

from fai_backend.vector.interface import IVector, OneOrMany, Embedding
from fai_backend.vector.types import Document, Where


class BaseVectorDB(IVector):
    def __init__(self, client: ClientAPI):
        self.client = client

    async def add(
            self,
            collection_name: str,
            ids: OneOrMany[str],
            embeddings: Optional[OneOrMany[Embedding]] = None,
            metadatas: Optional[OneOrMany[Mapping[str, Union[str, int, float, bool]]]] = None,
            documents: Optional[OneOrMany[str]] = None,
            uris: Optional[OneOrMany[str]] = None,
    ) -> None:
        collection = self.client.get_collection(name=collection_name)

        collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    async def update(
            self,
            collection_name: str,
            ids: OneOrMany[str],
            embeddings: Optional[OneOrMany[Embedding]] = None,
            metadatas: Optional[OneOrMany[Mapping[str, Union[str, int, float, bool]]]] = None,
            documents: Optional[OneOrMany[Document]] = None
    ) -> None:
        collection = self.client.get_collection(name=collection_name)
        collection.update(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    async def query(
            self,
            collection_name: str,
            query_embeddings: Optional[
                Union[
                    OneOrMany[Embedding],
                    OneOrMany[np.ndarray],
                ]
            ] = None,
            query_texts: Optional[OneOrMany[Document]] = None,
            n_results: int = 10,
            where: Optional[Where] = None,

    ) -> dict:
        collection = self.client.get_collection(name=collection_name)

        return collection.query(
            query_embeddings=query_embeddings,
            query_texts=query_texts,
            n_results=n_results,
            where=where,
        )

    async def get(
            self,
            collection_name: str,
            ids: Optional[OneOrMany[str]] = None,
    ):
        collection = self.client.get_collection(name=collection_name)

        return collection.get(
            ids=ids,
        )

    async def list_collections(self) -> Set[str]:
        collections = self.client.list_collections()

        collection_names = set()
        for collection in collections:
            collection_names.add(collection.name)

        return collection_names

    async def reset(self) -> bool:
        return self.client.reset()

    async def create_collection(self, collection_name: str):
        return self.client.create_collection(name=collection_name)

    async def delete_collection(self, collection_name: str):
        return self.client.delete_collection(name=collection_name)
