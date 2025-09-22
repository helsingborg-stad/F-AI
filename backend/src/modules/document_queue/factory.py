from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.document_queue.LocalFileDocumentQueueService import LocalFileDocumentQueueService
from src.modules.document_queue.protocols.IDocumentQueueService import IDocumentQueueService
from src.modules.vector.protocols.IVectorService import IVectorService


class DocumentQueueServiceFactory:
    def __init__(self, chunker_factory: DocumentChunkerFactory, vector_service: IVectorService):
        self._chunker_factory = chunker_factory
        self._vector_service = vector_service

    def get(self) -> IDocumentQueueService:
        return LocalFileDocumentQueueService(chunker_factory=self._chunker_factory, vector_service=self._vector_service)
