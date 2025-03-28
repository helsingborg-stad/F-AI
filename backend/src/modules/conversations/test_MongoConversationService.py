import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.conversations.MongoConversationService import MongoConversationService
from src.modules.conversations.test_conversation_service import BaseConversationServiceTestClass


@pytest_asyncio.fixture
def service(mongo_test_db: AsyncDatabase):
    return MongoConversationService(mongo_test_db)


class TestMongoConversationServiceClass(BaseConversationServiceTestClass):
    ...
