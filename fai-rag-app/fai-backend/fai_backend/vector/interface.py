from typing import Optional, Mapping, Union, Protocol, TypeVar

import numpy as np

from fai_backend.vector.types import OneOrMany, Embedding, Document, Where

T = TypeVar('T')


class IVector(Protocol[T]):
    def heartbeat(self) -> int:
        raise NotImplementedError('heartbeat not implemented')

    def reset(self) -> bool:
        raise NotImplementedError('reset not implemented')

    def delete(self, collection_name: str) -> None:
        raise NotImplementedError('delete not implemented')

    def add(
        self,
        collection_name: str,
        ids: OneOrMany[str],
        embeddings: Optional[OneOrMany[Embedding]] = None,
        metadatas: Optional[OneOrMany[Mapping[str, Union[str, int, float, bool]]]] = None,
        documents: Optional[OneOrMany[str]] = None,
        uris: Optional[OneOrMany[str]] = None,
    ) -> None:
        raise NotImplementedError('add not implemented')

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
    ) -> T:
        raise NotImplementedError('query not implemented')

    def list_collections(self) -> T:
        raise NotImplementedError('list_collections not implemented')

    def get_or_create_collection(self, collection_name: str) -> T:
        raise NotImplementedError('get_or_create_collection not implemented')

    def create_collection(self, collection_name: str) -> T:
        raise NotImplementedError('create_collection not implemented')
