import pytest

from src.modules.vector.models.VectorDocument import VectorDocument
from src.modules.vector.protocols.IVectorService import IVectorService


@pytest.mark.asyncio
async def test_basic_query(vector_service: IVectorService):
    doc1 = VectorDocument(
        id='doc1',
        content='hello world',
        metadata={'key1': 'lorem ipsum', 'key2': 'dolor sit amet'}
    )
    doc2 = VectorDocument(
        id='doc2',
        content='greetings world',
        metadata={'key1': 'lorem ipsum', 'key2': 'dolor sit amet'}
    )

    await vector_service.create_vector_space('test_space', 'default')
    await vector_service.add_documents_to_vector_space('test_space', 'default', [doc1, doc2])

    result = await vector_service.query_vector_space('test_space', 'default', 'hey', 10)

    assert doc1 in result
    assert doc2 in result


@pytest.mark.asyncio
async def test_query_max_results(vector_service: IVectorService):
    doc1 = VectorDocument(id='a', content='A', metadata=None)
    doc2 = VectorDocument(id='aa', content='AA', metadata=None)
    doc3 = VectorDocument(id='z', content='z', metadata=None)

    await vector_service.create_vector_space('test_space', 'default')
    await vector_service.add_documents_to_vector_space('test_space', 'default', [doc1, doc2, doc3])
    result = await vector_service.query_vector_space('test_space', 'default', 'a', 2)

    assert doc1 in result
    assert doc2 in result
    assert doc3 not in result


@pytest.mark.asyncio
async def test_delete(vector_service: IVectorService):
    doc = VectorDocument(id='a', content='A', metadata=None)

    await vector_service.create_vector_space('test_space', 'default')
    await vector_service.add_documents_to_vector_space('test_space', 'default', [doc])
    await vector_service.delete_vector_space('test_space')

    result = await vector_service.query_vector_space('test_space', 'default', 'a', 1)

    assert len(result) == 0


@pytest.mark.asyncio
async def test_create_twice(vector_service: IVectorService):
    await vector_service.create_vector_space('test_space', 'default')
    await vector_service.create_vector_space('test_space', 'default')
    assert True


@pytest.mark.asyncio
async def test_delete_twice(vector_service: IVectorService):
    await vector_service.create_vector_space('test_space', 'default')
    await vector_service.delete_vector_space('test_space')
    await vector_service.delete_vector_space('test_space')
    assert True


@pytest.mark.asyncio
async def test_delete_nonexisting(vector_service: IVectorService):
    await vector_service.delete_vector_space('does not exist')
    assert True
