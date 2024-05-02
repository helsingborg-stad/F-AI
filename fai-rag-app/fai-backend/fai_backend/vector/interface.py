from typing import Optional, Mapping, Union, Protocol, TypeVar

import numpy as np

from fai_backend.vector.types import OneOrMany, Embedding, Document, Where

T = TypeVar('T')


class IVector(Protocol[T]):
    def heartbeat(self) -> int:
        raise NotImplementedError('heartbeat not implemented')

    async def reset(self) -> bool:
        raise NotImplementedError('reset not implemented')

    async def add(
        self,
        collection_name: str,
        ids: OneOrMany[str],
        embeddings: Optional[OneOrMany[Embedding]] = None,
        metadatas: Optional[OneOrMany[Mapping[str, Union[str, int, float, bool]]]] = None,
        documents: Optional[OneOrMany[str]] = None,
        uris: Optional[OneOrMany[str]] = None,
    ) -> None:
        raise NotImplementedError('add not implemented')

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
    ) -> T:
        raise NotImplementedError('query not implemented')

    async def list_collections(self) -> T:
        raise NotImplementedError('list_collections not implemented')

    async def get_collection(self, name: str) -> T:
        raise NotImplementedError('get_collection not implemented')

    async def get_or_create_collection(self, collection_name: str) -> T:
        raise NotImplementedError('get_or_create_collection not implemented')

    async def create_collection(self, name: str) -> T:
        raise NotImplementedError('create_collection not implemented')

    async def delete_collection(self, name: str) -> T:
        raise NotImplementedError('delete_collection not implemented')
