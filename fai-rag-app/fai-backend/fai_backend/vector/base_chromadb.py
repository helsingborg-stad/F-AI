from typing import Union, Optional, Mapping, Set
import numpy as np
from fai_backend.vector.interface import IVector, OneOrMany, Embedding
from fai_backend.vector.types import Document, Where


class BaseVectorDB(IVector):
    def __init__(self, client):
        self.client = client

    def add(
            self,
            collection_name: str,
            ids: OneOrMany[str],
            collections: Optional[OneOrMany[str]] = None,
            embeddings: Optional[OneOrMany[Embedding]] = None,
            metadatas: Optional[OneOrMany[Mapping[str, Union[str, int, float, bool]]]] = None,
            documents: Optional[OneOrMany[str]] = None,
            uris: Optional[OneOrMany[str]] = None,
    ) -> None:
        collection = self.client.get_or_create_collection(collection_name)
        collection.add(
            documents=documents,
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

    def query(
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
        collection = self.client.get_or_create_collection(
            name=collection_name,
        )
        return collection.query(
            query_embeddings=query_embeddings,
            query_texts=query_texts,
            n_results=n_results,
            where=where,
        )

    def list_collections(self) -> Set[str]:
        collection = self.client.list_collections()

        collection_names = set()
        for collection in collection:
            collection_names.add(collection.name)

        return collection_names

    def get(
            self,
            collection_name: str,
            ids: Optional[OneOrMany[str]] = None,
    ):
        collection = self.client.get_or_create_collection(collection_name)

        return collection.get(
            ids=ids,
        )

    def reset(self) -> bool:
        return self.client.reset()

    def create_collection(self, collection_name: str):
        return self.client.create_collection(collection_name)
