from typing import Generic, TypeVar

from fai_backend.repository.interface import IAsyncRepo

T = TypeVar('T')


class InMemoryRepo(Generic[T], IAsyncRepo[T]):
    def __init__(self):
        self._items: dict[int, T] = {}
        self._current_id: int = 0

    async def create(self, item: T) -> T:
        self._current_id += 1
        item.id = str(self._current_id)
        self._items[self._current_id] = item
        return item

    async def get(self, item_id: str) -> T | None:
        return self._items.get(int(item_id))

    async def list(self) -> list[T]:
        return list(self._items.values())

    async def update(self, item_id: str, item_data: dict) -> T | None:
        if int(item_id) in self._items:
            item = self._items[int(item_id)]
            for key, value in item_data.items():
                setattr(item, key, value)
            return item
        return None

    async def delete(self, item_id: str) -> T | None:
        return self._items.pop(int(item_id), None)
