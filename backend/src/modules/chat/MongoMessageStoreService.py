import datetime

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id, ensure_expiry_index
from src.modules.chat.protocols.IMessageStoreService import IMessageStoreService


class MongoMessageStoreService(IMessageStoreService):
    def __init__(self, database: AsyncDatabase):
        self._database = database
        self._expiry_seconds = 30

    async def init(self, expiry_seconds: int):
        self._expiry_seconds = expiry_seconds
        await ensure_expiry_index(self._database['stored_messages'], self._expiry_seconds)

    async def store_message(self, message: str) -> str:
        result = await self._database['stored_messages'].insert_one(
            {'createdAt': datetime.datetime.utcnow(), 'message': message}
        )
        return str(result.inserted_id)

    async def consume_message(self, stored_message_id: str) -> str | None:
        if not is_valid_mongo_id(stored_message_id):
            return None

        result = await self._database['stored_messages'].find_one(
            {'_id': ObjectId(stored_message_id)},
            projection=['createdAt', 'message']
        )

        # We need to check expiry manually as well since Mongo automatic expiry check only runs about every 60 seconds
        if result is None or (datetime.datetime.utcnow() - result['createdAt']).total_seconds() >= self._expiry_seconds:
            return None

        await self._database['stored_messages'].delete_one({'_id': ObjectId(stored_message_id)})

        return result['message']
