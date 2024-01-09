from typing import Protocol, TypeVar

T = TypeVar('T')


class IAsyncRepo(Protocol[T]):
    async def get(self, item_id: str) -> T | None:
        raise NotImplementedError('get not implemented')

    async def list(self) -> list[T]:
        raise NotImplementedError('list not implemented')

    async def create(self, item: T) -> T | None:
        raise NotImplementedError('create not implemented')

    async def update(self, item_id: str, item: dict) -> T | None:
        raise NotImplementedError('update not implemented')

    async def delete(self, item_id: str) -> T | None:
        raise NotImplementedError('delete not implemented')
