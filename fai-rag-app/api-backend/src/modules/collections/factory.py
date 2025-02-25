from pymongo.asynchronous.database import AsyncDatabase

from src.modules.collections.MongoCollectionService import MongoCollectionService
from src.modules.collections.protocols.ICollectionService import ICollectionService
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.vector.protocols.IVectorService import IVectorService


class CollectionServiceFactory:
    def __init__(
            self,
            mongo_database: AsyncDatabase,
            vector_service: IVectorService,
            chunker_factory: DocumentChunkerFactory
    ) -> None:
        self._mongo_database = mongo_database
        self._vector_service = vector_service
        self._chunker_factory = chunker_factory

    def get(self) -> ICollectionService:
        return MongoCollectionService(
            database=self._mongo_database,
            vector_service=self._vector_service,
            chunker_factory=self._chunker_factory
        )
