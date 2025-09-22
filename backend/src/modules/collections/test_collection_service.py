import os.path

import pytest

from src.modules.collections.protocols.ICollectionService import ICollectionService
from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.protocols.IVectorService import IVectorService


class BaseCollectionServiceTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_collection(service: ICollectionService):
        result = await service.create_collection('my label', 'default')

        assert len(result) > 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_collection(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')

        result = await service.get_collection(collection_id)

        assert result
        assert result.id == collection_id
        assert result.label == 'my label'
        assert result.embedding_model == 'default'
        assert len(result.documents) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_collection_invalid(service: ICollectionService):
        result = await service.get_collection('does not exist')

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_collection_label(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')

        result = await service.set_collection_label(collection_id, 'my new label')

        collection = await service.get_collection(collection_id)

        assert result is True
        assert collection.label == 'my new label'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_collection_label_invalid(service: ICollectionService):
        result = await service.set_collection_label('does not exist', 'my new label')

        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_collection_documents(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')

        result = await service.set_collection_documents(
            collection_id,
            ['https://www.example.com/', os.path.join(os.path.dirname(__file__), 'test_file.md')]
        )

        collection = await service.get_collection(collection_id)

        assert result is True
        assert len(collection.documents) == 2

        assert len(collection.documents[0].id) > 0
        assert collection.documents[0].name == 'https://www.example.com/'
        assert collection.documents[0].type == 'url'
        assert collection.documents[0].state == 'queued'

        assert len(collection.documents[1].id) > 0
        assert collection.documents[1].name == 'test_file.md'
        assert collection.documents[1].type == 'text/markdown'
        assert collection.documents[1].state == 'queued'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_collection_documents_invalid(service: ICollectionService):
        result = await service.set_collection_documents(
            'does not exist',
            [os.path.join(os.path.dirname(__file__), 'test_file.md')]
        )

        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_collection_document(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')
        await service.set_collection_documents(collection_id, [os.path.join(os.path.dirname(__file__), 'test_file.md')])

        collection1 = await service.get_collection(collection_id)
        document1 = collection1.documents[0]

        result1 = await service.update_collection_document(collection_id=collection_id, document_id=document1.id,
                                                           state='processing')
        collection2 = await service.get_collection(collection_id)
        document2 = collection2.documents[0]

        result2 = await service.update_collection_document(collection_id=collection_id, document_id=document1.id,
                                                           state='ready')
        collection3 = await service.get_collection(collection_id)
        document3 = collection3.documents[0]

        assert document1.state == 'queued'

        assert result1 is True
        assert document2.state == 'processing'

        assert result2 is True
        assert document3.state == 'ready'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_collection_document_invalid_collection(service: ICollectionService):
        result = await service.update_collection_document('does not exist', 'does not exist', 'processing')

        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_collection_document_invalid_document(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')
        await service.set_collection_documents(collection_id, [os.path.join(os.path.dirname(__file__), 'test_file.md')])

        result = await service.update_collection_document(collection_id=collection_id, document_id='does not exist',
                                                          state='processing')

        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_query_collection(service: ICollectionService, vector_service: IVectorService):
        collection_id = await service.create_collection('my label', 'default')
        await service.set_collection_documents(
            collection_id,
            [os.path.join(os.path.dirname(__file__), 'test_file.md')]
        )

        # Simulate add procedure - happens in a separate process in the "real" scenario
        await vector_service.add_documents_to_vector_space(
            space=collection_id,
            embedding_model='default',
            documents=[VectorDocument(
                id='testchunk',
                content='Content for unit test - do not remove',
                metadata={'source': 'test_file.md', 'page_number': 1}
            )])

        result = await service.query_collection(collection_id, query='test', max_results=1)

        assert len(result) == 1
        assert result[0].source == 'test_file.md'
        assert result[0].content == 'Content for unit test - do not remove'
        assert result[0].page_number == 1

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_query_collection_zero(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')
        await service.set_collection_documents(
            collection_id,
            [os.path.join(os.path.dirname(__file__), 'test_file.md')]
        )

        result = await service.query_collection(collection_id, query='test', max_results=0)

        assert len(result) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_query_collection_invalid(service: ICollectionService):
        result = await service.query_collection('does not exist', query='test', max_results=1)

        assert len(result) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_collection(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')

        await service.delete_collection(collection_id)

        result = await service.get_collection(collection_id)

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_collection_invalid(service: ICollectionService):
        await service.delete_collection('does not exist')

        result = await service.get_collection('does not exist')

        assert result is None
