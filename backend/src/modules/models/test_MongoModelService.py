import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.models.factory import ModelServiceFactory
from src.modules.models.test_model_service import BaseModelServiceTestClass


@pytest_asyncio.fixture
async def service(mongo_test_db: AsyncDatabase):
    """Create a MongoModelService instance for testing."""
    await mongo_test_db['chat_models'].drop()
    
    service = ModelServiceFactory(mongo_database=mongo_test_db).get()
    yield service
    
    await mongo_test_db['chat_models'].drop()


class TestMongoModelService(BaseModelServiceTestClass):
    """Test MongoModelService implementation."""
    pass