import os.path

import pytest

from src.modules.collections.protocols.ICollectionService import ICollectionService


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

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_collection_missing(service: ICollectionService):
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
    async def test_set_collection_label_missing(service: ICollectionService):
        result = await service.set_collection_label('does not exist', 'my new label')

        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_collection_documents(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')

        result = await service.set_collection_documents(
            collection_id,
            [os.path.join(os.path.dirname(__file__), 'test_file.md')]
        )

        collection = await service.get_collection(collection_id)

        assert result is True
        assert collection.files[0].name == 'test_file.md'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_collection_documents_missing(service: ICollectionService):
        result = await service.set_collection_documents(
            'does not exist',
            [os.path.join(os.path.dirname(__file__), 'test_file.md')]
        )

        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_query_collection(service: ICollectionService):
        collection_id = await service.create_collection('my label', 'default')
        await service.set_collection_documents(
            collection_id,
            [os.path.join(os.path.dirname(__file__), 'test_file.md')]
        )

        result = await service.query_collection(collection_id, query='test', max_results=1)

        assert len(result) == 1
        assert result[0].source == 'test_file.md'
        assert result[0].content == 'Content for unit test - do not remove'

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
    async def test_query_collection_missing(service: ICollectionService):
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
    async def test_delete_collection_missing(service: ICollectionService):
        await service.delete_collection('does not exist')

        result = await service.get_collection('does not exist')

        assert result is None
