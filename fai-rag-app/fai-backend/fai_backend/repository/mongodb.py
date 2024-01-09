from typing import Generic, TypeVar

from beanie import Document, PydanticObjectId
from bson.errors import InvalidId

from fai_backend.repository.interface import IAsyncRepo

T = TypeVar('T', bound=Document)


class MongoDBRepo(Generic[T], IAsyncRepo[T]):
    def __init__(self, document_model: type[T]):
        self.model = document_model

    async def list(self) -> list[T]:
        return await self.model.all().to_list()

    async def create(self, item: T) -> T:
        item.id = PydanticObjectId()
        await item.insert_one(item)
        return item

    async def get(self, item_id: str) -> T | None:
        try:
            object_id = self._str_to_object_id(item_id)
            return await self.model.find_one(self.model.id == object_id)
        except InvalidId:
            return None

    async def update(self, item_id: str, item_data: dict) -> T | None:
        object_id = self._str_to_object_id(item_id)
        item = await self.model.find_one(self.model.id == object_id)
        if item:
            for key, value in item_data.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            await item.save_changes()
            return item
        return None

    async def delete(self, item_id: str) -> T | None:
        object_id = self._str_to_object_id(item_id)
        item = await self.model.find_one(self.model.id == object_id)
        if item:
            await item.delete()
            return item
        return None

    def _str_to_object_id(self, item_id: str) -> PydanticObjectId:
        return PydanticObjectId(item_id)
