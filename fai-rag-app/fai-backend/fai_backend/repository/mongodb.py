from typing import Generic, TypeVar

from beanie import Document, PydanticObjectId, SortDirection
from bson.errors import InvalidId
from pydantic import BaseModel

from fai_backend.repository.interface import IAsyncRepo
from fai_backend.repository.query.component import (
    QueryComponent,
)

T = TypeVar('T', bound=BaseModel)
T_DB = TypeVar('T_DB', bound=Document)


class MongoDBRepo(Generic[T, T_DB], IAsyncRepo[T]):
    model: type[T]
    odm_model: type[T_DB]

    def __init__(self, model: type[T], odm_model: type[T_DB]):
        self.model = model
        self.odm_model = odm_model

    async def list(
            self,
            query: QueryComponent = None,
            sort_by: str = None,
            sort_order: str = 'asc'
    ) -> list[T]:
        def find_query(q: QueryComponent = None) -> dict:
            return adapt_query_component(q).to_mongo_query() if query else {}

        db_query = self.odm_model.find(find_query(query))

        if sort_by:
            direction = SortDirection.ASCENDING if sort_order == 'asc' else SortDirection.DESCENDING
            db_query = db_query.sort((sort_by, direction))
        return [self.model.model_validate(doc) for doc in await db_query.to_list()]

    async def create(self, item: T) -> T:
        item = item.model_dump()
        item['id'] = PydanticObjectId()
        item_in_db = await self.odm_model.model_validate(item).create()
        return self.model.model_validate(item_in_db)

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
