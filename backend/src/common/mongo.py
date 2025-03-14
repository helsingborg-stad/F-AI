from bson import ObjectId
from bson.errors import InvalidId


def is_valid_mongo_id(any_id: str) -> bool:
    try:
        ObjectId(any_id)
        return True
    except InvalidId:
        return False
