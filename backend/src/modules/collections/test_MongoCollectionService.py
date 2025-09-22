import threading

import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.collections.MongoCollectionService import MongoCollectionService
from src.modules.collections.test_collection_service import BaseCollectionServiceTestClass
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.document_queue.models.DocumentMeta import DocumentMeta
from src.modules.document_queue.protocols.IDocumentQueueService import IDocumentQueueService, DocumentCallbackType
from src.modules.vector.protocols.IVectorService import IVectorService


class MockQueueService(IDocumentQueueService):
    async def add_to_queue(self, document_filename_or_url: str, meta: DocumentMeta):
        pass

    async def run_queue_loop(self, stop_event: threading.Event):
        pass

    def add_document_callback(self, callback: DocumentCallbackType):
        pass


@pytest_asyncio.fixture
def service(vector_service: IVectorService, mongo_test_db: AsyncDatabase):
    chunker_factory = DocumentChunkerFactory()
    return MongoCollectionService(
        mongo_test_db,
        vector_service=vector_service,
        chunker_factory=chunker_factory,
        queue_service=MockQueueService()
    )


class TestMongoCollectionService(BaseCollectionServiceTestClass):
    ...
