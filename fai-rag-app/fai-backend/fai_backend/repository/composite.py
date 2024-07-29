from typing import Generic, TypeVar

from fai_backend.repository.interface import IAsyncRepo
from fai_backend.repository.query.component import QueryComponent

T = TypeVar('T')


class CompositeRepo(Generic[T], IAsyncRepo[T]):
    def __init__(self, repos: list[IAsyncRepo[T]]):
        self._repos = repos

    async def get(self, item_id: str) -> T | None:
        for repo in self._repos:
            item = await repo.get(item_id)
            if item is not None:
                return item
        return None

    async def list(self, query: QueryComponent = None, sort_by: str = None, sort_order: str = 'asc') -> list[T]:
        all_items = []
        for repo in self._repos:
            items = await repo.list()
            all_items.extend(items)
        return all_items

    async def create(self, item: T) -> T | None:
        for repo in self._repos:
            try:
                return await repo.create(item)
            except NotImplementedError:
                continue
        return None

    async def update(self, item: T) -> T | None:
        for repo in self._repos:
            try:
                return await repo.update(item)
            except NotImplementedError:
                continue
        return None

    async def update_id(self, item_id: str, item: dict) -> T | None:
        for repo in self._repos:
            try:
                updated_item = await repo.update_id(item_id, item)
                if updated_item is not None:
                    return updated_item
            except NotImplementedError:
                continue
        return None

    async def delete(self, item_id: str) -> T | None:
        for repo in self._repos:
            try:
                deleted_item = await repo.delete(item_id)
                if deleted_item is not None:
                    return deleted_item
            except NotImplementedError:
                continue
        return None
