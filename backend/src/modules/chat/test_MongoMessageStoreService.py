import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.chat.MongoMessageStoreService import MongoMessageStoreService
from src.modules.chat.test_message_store_service import BaseMessageStoreServiceTestClass


@pytest_asyncio.fixture
async def service(mongo_test_db: AsyncDatabase):
    service = MongoMessageStoreService(mongo_test_db)
    await service.init(expiry_seconds=1)
    return service


class TestMongoMessageStoreServiceClass(BaseMessageStoreServiceTestClass):
    ...
