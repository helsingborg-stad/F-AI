from typing import Union, Optional, Mapping, TypeVar, Generic

import chromadb
import numpy as np

from fai_backend.vector.interface import IVector, OneOrMany, Embedding
from fai_backend.vector.types import Document, Where


T = TypeVar('T')


class ChromaDBVector(Generic[T], IVector[T]):
    def __init__(self, db_directory: str):
        self.client = chromadb.PersistentClient(
            path=db_directory,
            settings=chromadb.Settings(
                anonymized_telemetry=False,  # opt out of telemetry
                allow_reset=True
            )
        )

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
