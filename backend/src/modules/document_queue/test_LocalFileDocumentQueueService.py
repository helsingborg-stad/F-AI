import os
import shutil
import tempfile
import typing
from unittest.mock import AsyncMock

import pytest

from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.document_chunker.models.Chunk import Chunk
from src.modules.document_chunker.protocols.IDocumentChunker import IDocumentChunker
from src.modules.document_queue.LocalFileDocumentQueueService import LocalFileDocumentQueueService
from src.modules.document_queue.models.DocumentMeta import DocumentMeta
from src.modules.document_queue.models.DocumentStateUpdate import DocumentStateUpdate
from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.models.VectorSpace import VectorSpace
from src.modules.vector.protocols.IVectorService import IVectorService


class MockChunker(IDocumentChunker):
    def __init__(self, should_fail: bool):
        self._should_fail = should_fail

    def chunk(self, path_or_url: str, name: str | None = None) -> list[Chunk]:
        if self._should_fail:
            raise Exception("Mock chunker failed")
        return []


class MockChunkerFactory:
    def __init__(self, should_fail: bool):
        self._should_fail = should_fail

    def get(self, _path_or_url: str) -> IDocumentChunker:
        return MockChunker(self._should_fail)


class MockVectorService(IVectorService):
    def __init__(self, should_fail: bool):
        self._should_fail = should_fail

    async def create_vector_space(self, space: str, embedding_model: str):
        pass

    async def add_documents_to_vector_space(self, space: str, embedding_model: str, documents: list[VectorDocument]):
        if self._should_fail:
            raise Exception("Mock vector service failed")

    async def delete_vector_space(self, space: str):
        pass

    async def get_vector_spaces(self) -> list[VectorSpace]:
        return []

    async def query_vector_space(
            self,
            space: str,
            embedding_model: str,
            query: str,
            max_results: int
    ) -> list[VectorDocument]:
        return []


@pytest.fixture
def tmp_dir():
    return tempfile.mkdtemp()


@pytest.fixture
def document_service(tmp_dir: str):
    try:
        service = LocalFileDocumentQueueService(
            chunker_factory=typing.cast(DocumentChunkerFactory,
                                        typing.cast(object, MockChunkerFactory(should_fail=False))),
            vector_service=MockVectorService(should_fail=False),
            queue_dir=os.path.join(tmp_dir, "_service")
        )
        yield service
    finally:
        shutil.rmtree(tmp_dir)


@pytest.fixture
def document_service_bad_chunk(tmp_dir: str):
    try:
        service = LocalFileDocumentQueueService(
            chunker_factory=typing.cast(DocumentChunkerFactory,
                                        typing.cast(object, MockChunkerFactory(should_fail=True))),
            vector_service=MockVectorService(should_fail=False),
            queue_dir=os.path.join(tmp_dir, "_service")
        )
        yield service
    finally:
        shutil.rmtree(tmp_dir)


@pytest.fixture
def document_service_bad_vector(tmp_dir: str):
    try:
        service = LocalFileDocumentQueueService(
            chunker_factory=typing.cast(DocumentChunkerFactory,
                                        typing.cast(object, MockChunkerFactory(should_fail=False))),
            vector_service=MockVectorService(should_fail=True),
            queue_dir=os.path.join(tmp_dir, "_service")
        )
        yield service
    finally:
        shutil.rmtree(tmp_dir)


async def setup_test(tmp_dir: str, document_service: LocalFileDocumentQueueService):
    tmp_file = os.path.join(tmp_dir, 'testfile.txt')
    with open(tmp_file, 'w') as f:
        f.write('test content')

    callback_mock = AsyncMock()
    document_service.add_document_callback(callback_mock)

    await document_service.add_to_queue(tmp_file, DocumentMeta(
        space_id='testspace',
        document_id='testfile',
        embedding_model='default',
        source_name='testfile.txt'
    ))

    return callback_mock


class TestLocalFileDocumentQueueService:
    @staticmethod
    @pytest.mark.asyncio
    async def test_queued_document_is_processed(tmp_dir: str, document_service: LocalFileDocumentQueueService):
        callback_mock = await setup_test(tmp_dir, document_service)

        assert len([f for f in os.scandir(document_service.get_queue_dir()) if f.is_file()]) == 2

        was_document_processed = await document_service.try_process_next_document()

        callback_mock.assert_any_call(DocumentStateUpdate(
            space_id='testspace',
            document_id='testfile',
            status='processing'
        ))
        callback_mock.assert_any_call(DocumentStateUpdate(
            space_id='testspace',
            document_id='testfile',
            status='ready'
        ))

        assert was_document_processed is True
        assert len([f for f in os.scandir(document_service.get_queue_dir()) if f.is_file()]) == 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_handle_bad_chunk(tmp_dir: str, document_service_bad_chunk: LocalFileDocumentQueueService):
        callback_mock = await setup_test(tmp_dir, document_service_bad_chunk)

        first_try = await document_service_bad_chunk.try_process_next_document()
        second_try = await document_service_bad_chunk.try_process_next_document()

        assert first_try is True
        assert second_try is False
        assert callback_mock.call_count == 2
        callback_mock.assert_called_with(DocumentStateUpdate(
            space_id='testspace',
            document_id='testfile',
            status='error'
        ))
        assert len([f for f in os.scandir(document_service_bad_chunk.get_queue_dir()) if f.is_file()]) == 0

    @staticmethod
    @pytest.mark.asyncio
    async def test_handle_bad_vector(tmp_dir: str, document_service_bad_vector: LocalFileDocumentQueueService):
        callback_mock = await setup_test(tmp_dir, document_service_bad_vector)

        first_try = await document_service_bad_vector.try_process_next_document()
        second_try = await document_service_bad_vector.try_process_next_document()

        assert first_try is True
        assert second_try is False
        callback_mock.assert_called_with(DocumentStateUpdate(
            space_id='testspace',
            document_id='testfile',
            status='error'
        ))
        assert callback_mock.call_count == 2
        assert len([f for f in os.scandir(document_service_bad_vector.get_queue_dir()) if f.is_file()]) == 0
