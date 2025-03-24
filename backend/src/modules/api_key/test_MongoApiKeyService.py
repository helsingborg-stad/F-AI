import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.api_key.MongoApiKeyService import MongoApiKeyService
from src.modules.api_key.test_api_key_service import BaseApiKeyTestClass


@pytest_asyncio.fixture
def service(mongo_test_db: AsyncDatabase):
    return MongoApiKeyService(mongo_test_db)


class TestMongoApiKeyServiceClass(BaseApiKeyTestClass):
    ...
