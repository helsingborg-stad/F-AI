from typing import Generic, TypeVar

from beanie import Document, PydanticObjectId
from bson.errors import InvalidId
from pydantic import BaseModel

from fai_backend.repository.interface import IAsyncRepo

T = TypeVar('T', bound=BaseModel)
T_DB = TypeVar('T_DB', bound=Document)


class MongoDBRepo(Generic[T, T_DB], IAsyncRepo[T]):
    model: type[T]
    odm_model: type[T_DB]

    def __init__(self, model: type[T], odm_model: type[T_DB]):
        self.model = model
        self.odm_model = odm_model

    async def list(self) -> list[T]:
        return await self.odm_model.all().to_list()

    async def create(self, item: T) -> T:
        item.id = PydanticObjectId()
        return self.model.model_validate(await self.odm_model.model_validate(item.model_dump()).create())

    async def get(self, item_id: str) -> T | None:
        try:
            item = await self.odm_model.find_one(self.odm_model.id == self._str_to_object_id(item_id))
            return self.model.model_validate(
                item
            ) if item else None
        except InvalidId:
            return None

    async def update(self, item_id: str, item_data: dict) -> T | None:
        object_id = self._str_to_object_id(item_id)
        item = await self.odm_model.find_one(self.odm_model.id == object_id)
        if item:
            for key, value in item_data.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            await item.save_changes()
            return self.model.model_validate(item)
        return None

    async def delete(self, item_id: str) -> T | None:
        object_id = self._str_to_object_id(item_id)
        item = await self.odm_model.find_one(self.odm_model.id == object_id)
        if item:
            await item.delete()
            return self.model.model_validate(item)
        return None

    def _str_to_object_id(self, item_id: str) -> PydanticObjectId:
        return PydanticObjectId(item_id)
