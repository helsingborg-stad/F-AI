import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.collections.MongoCollectionService import MongoCollectionService
from src.modules.collections.test_collection_service import BaseCollectionServiceTestClass
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.vector.protocols.IVectorService import IVectorService


@pytest_asyncio.fixture
def service(vector_service: IVectorService, mongo_test_db: AsyncDatabase):
    return MongoCollectionService(
        mongo_test_db,
        vector_service=vector_service,
        chunker_factory=DocumentChunkerFactory(),
    )


class TestMongoCollectionService(BaseCollectionServiceTestClass):
    ...
