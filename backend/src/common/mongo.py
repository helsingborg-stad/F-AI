from bson import ObjectId
from bson.errors import InvalidId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.errors import OperationFailure


def is_valid_mongo_id(any_id: str) -> bool:
    try:
        ObjectId(any_id)
        return True
    except InvalidId:
        return False


async def ensure_expiry_index(collection: AsyncCollection, expiry_seconds: int):
    try:
        await collection.drop_index('_expiry')
    except OperationFailure as e:
        if e.code != 27:  # IndexNotFound
            raise e
    await collection.create_index('createdAt', name='_expiry',
                                  expireAfterSeconds=expiry_seconds)
