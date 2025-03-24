import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.assistants.MongoAssistantService import MongoAssistantService
from src.modules.assistants.test_assistant_service import BaseAssistantServiceTestClass


@pytest_asyncio.fixture
def service(mongo_test_db: AsyncDatabase):
    return MongoAssistantService(mongo_test_db)


class TestMongoAssistantService(BaseAssistantServiceTestClass):
    ...
