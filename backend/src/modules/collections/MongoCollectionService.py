from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.is_url import is_url
from src.common.mongo import is_valid_mongo_id
from src.modules.collections.models.CollectionFile import CollectionFile
from src.modules.collections.models.CollectionMetadata import CollectionMetadata
from src.modules.collections.models.CollectionQueryResult import CollectionQueryResult
from src.modules.collections.protocols.ICollectionService import ICollectionService
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.protocols.IVectorService import IVectorService


class MongoCollectionService(ICollectionService):
    def __init__(self, database: AsyncDatabase, vector_service: IVectorService,
                 chunker_factory: DocumentChunkerFactory):
        self._database = database
        self._vector_service = vector_service
        self._chunker_factory = chunker_factory

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
                                                              projection=['_id', 'label', 'embedding_model', 'files',
                                                                          'urls'])
        if result is None:
            return None

        return CollectionMetadata(
            id=str(result['_id']),
            label=result['label'],
            embedding_model=result['embedding_model'],
            files=result['files'],
            urls=result['urls']
        )

    async def get_collections(self) -> list[CollectionMetadata]:
        cursor = self._database['collections'].find(projection=['_id', 'label', 'embedding_model', 'files', 'urls'])
        return [CollectionMetadata(
            id=str(doc['_id']),
            label=doc['label'],
            embedding_model=doc['embedding_model'],
            files=doc['files'],
            urls=doc['urls']
        )
            async for doc in cursor
        ]

    async def set_collection_label(self, collection_id: str, label: str) -> bool:
        if not is_valid_mongo_id(collection_id):
            return False

        result = await self._database['collections'].update_one(
            {'_id': ObjectId(collection_id)},
            {
                '$set': {'label': label}
            })
        return result.modified_count == 1

    async def set_collection_documents(self, collection_id: str, paths_and_urls: list[str]) -> bool:
        await self._vector_service.delete_vector_space(collection_id)

        collection_meta = await self.get_collection(collection_id)

        if collection_meta is None:
            return False

        await self._vector_service.create_vector_space(collection_id, collection_meta.embedding_model)

        urls = []
        files = []

        for path_or_url in paths_and_urls:
            chunker_service = self._chunker_factory.get(path_or_url)
            chunks = chunker_service.chunk(path_or_url)

            if len(chunks) == 0:
                continue

            if is_url(path_or_url):
                urls.append(path_or_url)
            else:
                files.append(CollectionFile(name=chunks[0].source))

            documents = [VectorDocument(
                id=chunk.id,
                content=chunk.content,
                metadata={
                    'source': chunk.source,
                    'page_number': chunk.page_number or -1
                }
            ) for chunk in chunks]

            await self._vector_service.add_documents_to_vector_space(
                space=collection_id,
                embedding_model=collection_meta.embedding_model,
                documents=documents
            )

        result = await self._database['collections'].update_one({
            '_id': ObjectId(collection_id)
        }, {
            '$set': {
                'urls': urls,
                'files': [file.model_dump() for file in files]
            }
        })

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
