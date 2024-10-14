from random import random

import pytest
import pytest_asyncio
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient

from fai_backend.collection.models import CollectionMetadataModel
from fai_backend.collection.service import CollectionService
from fai_backend.repositories import collection_metadata_repo
from fai_backend.repository.mongodb import MongoDBRepo
from fai_backend.vector.memory import InMemoryChromaDB
from fai_backend.vector.service import VectorService


@pytest_asyncio.fixture
async def collection_meta_repo():
    await init_beanie(database=(AsyncMongoMockClient()).test_db, document_models=[CollectionMetadataModel])
    yield MongoDBRepo[CollectionMetadataModel, CollectionMetadataModel](CollectionMetadataModel,
                                                                        CollectionMetadataModel)
    await CollectionMetadataModel.get_motor_collection().drop()


@pytest_asyncio.fixture
async def collection_meta_service(collection_meta_repo):
    yield CollectionService(collection_metadata_repo)


@pytest_asyncio.fixture
async def memory_vector_db():
    db_instance = InMemoryChromaDB()
    yield db_instance
    await db_instance.reset()


@pytest_asyncio.fixture
async def vector_service(memory_vector_db, collection_meta_service):
    return VectorService(memory_vector_db, collection_meta_service)


@pytest.mark.asyncio
async def test_add(memory_vector_db):
    collection_name = 'test_collection'
    await memory_vector_db.create_collection(collection_name=collection_name)

    await memory_vector_db.add(
        collection_name=collection_name,
        embeddings=[[random() for _ in range(384)] for _ in range(2)],
        documents=['This is a document', 'This is another document'],
        metadatas=[{'source': 'my_source'}, {'source': 'my_source'}],
        ids=['id1', 'id2']
    )

    get_embedding_by_id = await memory_vector_db.get(collection_name=collection_name, ids=['id1'])

    assert get_embedding_by_id['ids'] == ['id1']
    assert get_embedding_by_id['metadatas'] == [{'source': 'my_source'}]
    assert get_embedding_by_id['documents'] == ['This is a document']


@pytest.mark.asyncio
async def test_query(memory_vector_db):
    collection_name = 'test_collection'
    await memory_vector_db.create_collection(collection_name=collection_name)

    await memory_vector_db.add(
        collection_name=collection_name,
        documents=['Dog', 'Chair'],
        metadatas=[{'source': 'my_source'}, {'source': 'my_source'}],
        ids=['id1', 'id2']
    )

    results = await memory_vector_db.query(
        collection_name=collection_name,
        query_texts=['Animal'],
        n_results=1
    )

    assert results['ids'] == [['id1']]


@pytest.mark.asyncio
async def test_query_service_add(memory_vector_db, vector_service):
    collection_name = 'test_collection'

    await vector_service.create_collection(collection_name=collection_name)

    await vector_service.add_to_collection(
        collection_name=collection_name,
        documents=['Dog', 'Chair'],
        ids=['id1', 'id2']
    )

    result = await vector_service.query_from_collection(
        collection_name=collection_name,
        query_texts=['Animal'],
        n_results=1
    )

    assert result['ids'] == [['id1']]


@pytest.mark.asyncio
async def test_add_two_collections_then_correctly_list_all_added_collections(memory_vector_db, collection_meta_service):
    collection1_vector_service = VectorService(vector_db=memory_vector_db,
                                               collection_meta_service=collection_meta_service)
    await collection1_vector_service.create_collection(collection_name='collection1')

    collection2_vector_service = VectorService(vector_db=memory_vector_db,
                                               collection_meta_service=collection_meta_service)
    await collection2_vector_service.create_collection(collection_name='collection2')

    await collection1_vector_service.add_to_collection(
        collection_name='collection1',
        documents=['Chair', 'Table'],
        ids=['id1', 'id2']
    )

    await collection2_vector_service.add_to_collection(
        collection_name='collection2',
        documents=['Cat', 'Dog'],
        ids=['id1', 'id2']
    )

    listed_collections = await collection1_vector_service.list_collections()
    assert set(listed_collections) == {'collection1', 'collection2'}


@pytest.mark.asyncio
async def test_update_id_document_and_expect_update(memory_vector_db, collection_meta_service):
    collection_name = 'test_collection'

    # Setup initial data
    vector_service = VectorService(vector_db=memory_vector_db, collection_meta_service=collection_meta_service)
    await vector_service.create_collection(collection_name=collection_name)
    await vector_service.add_to_collection(
        collection_name=collection_name,
        documents=['Cat', 'Dog'],
        ids=['id1', 'id2']
    )

    # Update the document for id1
    await vector_service.add_to_collection(
        collection_name=collection_name,
        documents=['Chair'],
        ids=['id1']
    )

    query_updated_document = await vector_service.query_from_collection(
        collection_name=collection_name,
        query_texts=['Chair'],
        n_results=1
    )

    assert query_updated_document['ids'] == [['id1']]

    query_non_updated_document = await vector_service.query_from_collection(
        collection_name=collection_name,
        query_texts=['Dog'],
        n_results=1
    )

    assert query_non_updated_document['ids'] == [['id2']]


@pytest.mark.asyncio
async def test_add_documents_without_id_to_collection_then_query_correct_result(vector_service):
    collection_name = 'animal_collection'
    documents = ['Cat', 'Dog']

    await vector_service.create_collection(collection_name)
    await vector_service.add_documents_without_id_to_empty_collection(collection_name, documents)

    results = await vector_service.query_from_collection(
        collection_name=collection_name,
        query_texts=['Cat'],
        n_results=1
    )

    assert results['ids'] == [['0']]
