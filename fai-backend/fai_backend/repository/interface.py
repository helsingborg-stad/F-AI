from typing import Protocol, TypeVar

from fai_backend.repository.query.component import QueryComponent

T = TypeVar('T')


class IAsyncRepo(Protocol[T]):
    async def get(self, item_id: str) -> T | None:
        raise NotImplementedError('get not implemented')

    async def list(self, query: QueryComponent = None, sort_by: str = None, sort_order: str = 'asc') -> list[T]:
        raise NotImplementedError('list not implemented')

    async def create(self, item: T) -> T | None:
        raise NotImplementedError('create not implemented')

    async def update(self, item_id: str, item: dict) -> T | None:
        raise NotImplementedError('update not implemented')

    async def delete(self, item_id: str) -> T | None:
        raise NotImplementedError('delete not implemented')
