from collections.abc import Callable, Mapping
from typing import Optional, Union

import numpy as np
from chromadb import ClientAPI, EmbeddingFunction

from fai_backend.vector.embedding import EmbeddingFnFactory
from fai_backend.vector.interface import Embedding, IVector, OneOrMany
from fai_backend.vector.types import Document, Where


class BaseChromaDB(IVector):
    def __init__(self, client: ClientAPI):
        self.client = client

    def _get_collection(self, collection_name: str, embedding_function: EmbeddingFunction | None = None):
        return self.client.get_collection(
            name=collection_name,
            embedding_function=embedding_function or EmbeddingFnFactory.create('default')
        )

    async def add(
            self,
            collection_name: str,
            ids: OneOrMany[str],
            embeddings: Optional[OneOrMany[Embedding]] = None,
            metadatas: Optional[OneOrMany[Mapping[str, Union[str, int, float, bool]]]] = None,
            documents: Optional[OneOrMany[str]] = None,
            uris: Optional[OneOrMany[str]] = None,
            embedding_function: Callable[[str], np.ndarray] | None = None,
    ) -> None:
        collection = self._get_collection(collection_name, embedding_function)

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
            documents: Optional[OneOrMany[Document]] = None,
            embedding_function: Callable[[str], np.ndarray] | None = None,
    ) -> None:
        collection = self._get_collection(collection_name, embedding_function)
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
            embedding_function: Callable[[str], np.ndarray] | None = None,
    ) -> dict:
        collection = self._get_collection(collection_name, embedding_function)

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
            embedding_function: Callable[[str], np.ndarray] | None = None,
    ):
        collection = self._get_collection(
            collection_name,
            embedding_function
        )

        return collection.get(
            ids=ids,
        )

    async def list_collections(self) -> set[str]:
        collections = self.client.list_collections()
        return {collection.name for collection in collections}

    async def reset(self) -> bool:
        return self.client.reset()

    async def create_collection(self, collection_name: str,
                                embedding_function: Callable[[str], np.ndarray] | None = None):
        return self.client.create_collection(
            name=collection_name,
            embedding_function=embedding_function or EmbeddingFnFactory.create('default')
        )

    async def delete_collection(self, collection_name: str):
        return self.client.delete_collection(name=collection_name)
