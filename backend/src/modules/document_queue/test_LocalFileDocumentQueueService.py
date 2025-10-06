import asyncio
import os
import threading
from unittest.mock import Mock, patch, AsyncMock
import pytest

from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.document_queue.LocalFileDocumentQueueService import LocalFileDocumentQueueService
from src.modules.document_queue.models.DocumentMeta import DocumentMeta
from src.modules.vector.protocols.IVectorService import IVectorService


@pytest.mark.asyncio
async def test_file_cleanup_failure_causes_reprocessing(tmp_path):
    """
    Test if os.remove() fails on the meta file, the same file gets reprocessed infinitely.
    """
    temp_dir = str(tmp_path)

    mock_vector_service = Mock(spec=IVectorService)
    mock_vector_service.add_documents_to_vector_space = AsyncMock()

    mock_chunker = Mock()
    mock_chunker.chunk = Mock(side_effect=Exception("Simulated chunking error"))

    mock_chunker_factory = Mock(spec=DocumentChunkerFactory)
    mock_chunker_factory.get = Mock(return_value=mock_chunker)

    service = LocalFileDocumentQueueService(
        chunker_factory=mock_chunker_factory,
        vector_service=mock_vector_service
    )
    service._queue_dir = temp_dir

    test_file = os.path.join(temp_dir, "test_input.txt")
    with open(test_file, "w") as f:
        f.write("test content")

    meta = DocumentMeta(
        space_id="test_space",
        document_id="test_doc",
        embedding_model="test_model",
        source_name="test.txt"
    )

    await service.add_to_queue(test_file, meta)

    processing_attempts = []

    original_remove = os.remove

    def mock_remove(path):
        """Mock os.remove to fail on meta file removal"""
        if path.endswith('.meta'):
            processing_attempts.append(path)
            raise PermissionError(f"Simulated permission denied on {path}")
        else:
            return original_remove(path)

    stop_event = threading.Event()

    with patch('os.remove', side_effect=mock_remove):
        task = asyncio.create_task(service.run_queue_loop(stop_event))

        for _ in range(50):
            await asyncio.sleep(0.1)
            if len(processing_attempts) >= 3:
                break

        stop_event.set()

        try:
            await asyncio.wait_for(task, timeout=2.0)
        except asyncio.TimeoutError:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    assert len(processing_attempts) >= 2, \
        f"Expected file to be reprocessed at least twice, but got {len(processing_attempts)} attempts"

    assert len(set(processing_attempts)) == 1, \
        "All processing attempts should be for the same meta file"

    print(f"✓ Issue confirmed: File was reprocessed {len(processing_attempts)} times due to cleanup failure")


@pytest.mark.asyncio
async def test_file_cleanup_failure_leaves_files_in_queue(tmp_path):
    """
    Test that demonstrates files remain in queue when cleanup fails.
    """
    temp_dir = str(tmp_path)

    mock_vector_service = Mock(spec=IVectorService)
    mock_vector_service.add_documents_to_vector_space = AsyncMock()

    mock_chunker = Mock()
    mock_chunker.chunk = Mock(side_effect=Exception("Simulated error"))

    mock_chunker_factory = Mock(spec=DocumentChunkerFactory)
    mock_chunker_factory.get = Mock(return_value=mock_chunker)

    service = LocalFileDocumentQueueService(
        chunker_factory=mock_chunker_factory,
        vector_service=mock_vector_service
    )
    service._queue_dir = temp_dir

    test_file = os.path.join(temp_dir, "test_input.txt")
    with open(test_file, "w") as f:
        f.write("test content")

    meta = DocumentMeta(
        space_id="test_space",
        document_id="test_doc",
        embedding_model="test_model",
        source_name="test.txt"
    )

    await service.add_to_queue(test_file, meta)

    meta_files_before = [f for f in os.listdir(temp_dir) if f.endswith('.meta')]
    assert len(meta_files_before) == 1

    original_remove = os.remove

    def mock_remove(path):
        if path.endswith('.meta'):
            raise PermissionError("Cannot remove meta file")
        return original_remove(path)

    stop_event = threading.Event()

    with patch('os.remove', side_effect=mock_remove):
        task = asyncio.create_task(service.run_queue_loop(stop_event))

        await asyncio.sleep(0.5)

        stop_event.set()

        try:
            await asyncio.wait_for(task, timeout=2.0)
        except asyncio.TimeoutError:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    meta_files_after = [f for f in os.listdir(temp_dir) if f.endswith('.meta')]
    assert len(meta_files_after) == 1, \
        "Meta file should still exist in queue after cleanup failure"

    print("✓ Issue confirmed: Files remain in queue when cleanup fails")
