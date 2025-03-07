import uuid
from collections.abc import Mapping
from typing import Any

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.hashing import hash_secret
from src.common.mongo import is_valid_mongo_id
from src.modules.api_key.models.NewlyCreatedApiKey import NewlyCreatedApiKey
from src.modules.api_key.models.RedactedApiKey import RedactedApiKey
from src.modules.api_key.models.StoredApiKey import StoredApiKey
from src.modules.api_key.protocols.IApiKeyService import IApiKeyService


class MongoApiKeyService(IApiKeyService):
    def __init__(self, database: AsyncDatabase):
        self._database = database

    async def create(self, scopes: list[str]) -> NewlyCreatedApiKey:
        new_id = ObjectId()
        key = f'fai-{uuid.uuid4().hex}.{str(new_id)}'
        key_hash = hash_secret(key)
        key_hint = self._create_key_hint(key)
        api_key = StoredApiKey(
            key_hash=key_hash,
            key_hint=key_hint,
            scopes=scopes)

        result = await self._database['api_key'].insert_one({
            **api_key.model_dump(),
            '_id': new_id
        })

        return NewlyCreatedApiKey(
            revoke_id=str(result.inserted_id),
            api_key=key
        )

    async def revoke(self, revoke_id: str):
        if not is_valid_mongo_id(revoke_id):
            return

        await self._database['api_key'].delete_one({'_id': ObjectId(revoke_id)})

    async def get_all(self) -> list[RedactedApiKey]:
        cursor = self._database['api_key'].find(projection=['_id', 'key_hint', 'scopes'])
        return [self._to_read_only_api_key(doc) async for doc in cursor]

    async def find_by_key(self, key: str) -> RedactedApiKey | None:
        if '.' not in key:
            return None

        (api_key, lookup_id) = key.split('.')
        if not is_valid_mongo_id(lookup_id):
            return None

        result = await self._database['api_key'].find_one({'_id': ObjectId(lookup_id)})
        return self._to_read_only_api_key(result) if result else None

    async def find_by_revoke_id(self, revoke_id: str) -> RedactedApiKey | None:
        if not is_valid_mongo_id(revoke_id):
            return None

        result = await self._database['api_key'].find_one({'_id': ObjectId(revoke_id)})
        return self._to_read_only_api_key(result) if result else None

    @staticmethod
    def _to_read_only_api_key(db_doc: Mapping[str, Any]) -> RedactedApiKey:
        return RedactedApiKey(
            revoke_id=str(db_doc['_id']),
            key_hint=db_doc['key_hint'],
            scopes=db_doc['scopes'],
        )

    @staticmethod
    def _create_key_hint(key: str) -> str:
        return key[:8] + "..." + key[-4:]
