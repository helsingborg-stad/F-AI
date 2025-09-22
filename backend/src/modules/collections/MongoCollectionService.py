from typing import Mapping, Any, Literal

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.is_url import is_url
from src.common.mongo import is_valid_mongo_id
from src.modules.collections.models.CollectionDocument import CollectionDocument
from src.modules.collections.models.CollectionMetadata import CollectionMetadata
from src.modules.collections.models.CollectionQueryResult import CollectionQueryResult
from src.modules.collections.protocols.ICollectionService import ICollectionService
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.document_chunker.helpers.get_mime_type import get_mime_type
from src.modules.document_queue.models.DocumentMeta import DocumentMeta
from src.modules.document_queue.protocols.IDocumentQueueService import IDocumentQueueService, DocumentStateUpdate
from src.modules.vector.protocols.IVectorService import IVectorService


class MongoCollectionService(ICollectionService):
    def __init__(self, database: AsyncDatabase, vector_service: IVectorService,
                 chunker_factory: DocumentChunkerFactory, queue_service: IDocumentQueueService):
        self._database = database
        self._vector_service = vector_service
        self._chunker_factory = chunker_factory
        self._queue_service = queue_service
        queue_service.add_document_callback(self._update_document_state)

    async def create_collection(self, label: str, embedding_model: str) -> str:
        new_id = ObjectId()
        await self._vector_service.create_vector_space(str(new_id), embedding_model)
        await self._database['collections'].insert_one({
            '_id': new_id,
            'label': label,
            'embedding_model': embedding_model,
            'files': [],
            'urls': []
        })
        return str(new_id)

    async def get_collection(self, collection_id: str) -> CollectionMetadata | None:
        if not is_valid_mongo_id(collection_id):
            return None

        result = await self._database['collections'].find_one({'_id': ObjectId(collection_id)},
                                                              projection=['_id', 'label', 'embedding_model',
                                                                          'documents'])
        if result is None:
            return None

        return self._doc_to_collection_metadata(result)

    async def get_collections(self) -> list[CollectionMetadata]:
        cursor = self._database['collections'].find(projection=['_id', 'label', 'embedding_model', 'documents'])
        return [self._doc_to_collection_metadata(doc) async for doc in cursor]

    async def set_collection_label(self, collection_id: str, label: str) -> bool:
        if not is_valid_mongo_id(collection_id):
            return False

        result = await self._database['collections'].update_one(
            {'_id': ObjectId(collection_id)},
            {
                '$set': {'label': label}
            })
        return result.matched_count == 1

    async def set_collection_documents(self, collection_id: str, paths_and_urls: list[str]) -> bool:
        await self._vector_service.delete_vector_space(collection_id)

        collection_meta = await self.get_collection(collection_id)

        if collection_meta is None:
            return False

        await self._vector_service.create_vector_space(collection_id, collection_meta.embedding_model)

        contents: list[CollectionDocument] = []

        for path_or_url in paths_and_urls:
            document_id = str(ObjectId())
            document_name = path_or_url.split('/')[-1] if not is_url(path_or_url) else path_or_url
            contents.append(CollectionDocument(
                id=document_id,
                name=document_name,
                type=get_mime_type(path_or_url) if not is_url(path_or_url) else 'url',
                state='queued',
            ))
            await self._queue_service.add_to_queue(path_or_url,
                                                   DocumentMeta(
                                                       space_id=collection_id,
                                                       document_id=document_id,
                                                       embedding_model=collection_meta.embedding_model,
                                                       source_name=document_name)
                                                   )

        result = await self._database['collections'].update_one(
            {'_id': ObjectId(collection_id)},
            {'$set': {'documents': [c.model_dump() for c in contents]}}
        )

        return result.modified_count == 1

    async def update_collection_document(self, collection_id: str, document_id: str,
                                         state: Literal['queued', 'processing', 'ready', 'error']) -> bool:
        if not is_valid_mongo_id(collection_id):
            return False

        result = await self._database['collections'].update_one(
            {'_id': ObjectId(collection_id)},
            {'$set': {'documents.$[doc].state': state}},
            array_filters=[{'doc.id': document_id}]
        )

        return result.modified_count == 1

    async def query_collection(self, collection_id: str, query: str, max_results: int) -> list[CollectionQueryResult]:
        collection_meta = await self.get_collection(collection_id)

        if collection_meta is None or max_results <= 0:
            return []

        results = await self._vector_service.query_vector_space(
            space=collection_id,
            embedding_model=collection_meta.embedding_model,
            query=query,
            max_results=max_results
        )
        return [
            CollectionQueryResult(
                content=result.content,
                source=result.metadata['source'],
                page_number=None if result.metadata['page_number'] == -1 else result.metadata['page_number']
            ) for result in results
        ]

    async def delete_collection(self, collection_id: str):
        await self._vector_service.delete_vector_space(collection_id)

        if is_valid_mongo_id(collection_id):
            await self._database['collections'].delete_one({'_id': ObjectId(collection_id)})

    async def _update_document_state(self, document_state: DocumentStateUpdate):
        print(
            f"MongoCollectionService._update_document_state: {document_state.space_id} {document_state.document_id} {document_state.status}")
        await self._database['collections'].update_one(
            {'_id': ObjectId(document_state.space_id)},
            {'$set': {'documents.$[doc].state': document_state.status}},
            array_filters=[{'doc.id': document_state.document_id}]
        )

    @staticmethod
    def _doc_to_collection_metadata(doc: Mapping[str, Any]) -> CollectionMetadata:
        return CollectionMetadata(
            id=str(doc['_id']),
            label=doc['label'],
            embedding_model=doc['embedding_model'],
            documents=doc['documents'] if 'documents' in doc else [],
        )
