import pytest

from fai_backend.vector.memory import InMemoryVectorDB
from fai_backend.vector.service import VectorService


@pytest.fixture
def memory_vector_db():
    db_instance = InMemoryVectorDB()
    yield db_instance
    db_instance.reset()


@pytest.mark.asyncio
async def test_add(memory_vector_db):
    collection_name = "test_collection"
    memory_vector_db.add(
        collection_name=collection_name,
        embeddings=[[1.2, 2.3, 4.5], [6.7, 8.2, 9.2]],
        documents=["This is a document", "This is another document"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )

    get_embedding_by_id = memory_vector_db.get(collection_name=collection_name, ids=["id1"])

    assert get_embedding_by_id["ids"] == ["id1"]
    assert get_embedding_by_id["metadatas"] == [{"source": "my_source"}]
    assert get_embedding_by_id["documents"] == ["This is a document"]


@pytest.mark.asyncio
async def test_query(memory_vector_db):
    collection_name = "test_collection"
    memory_vector_db.add(
        collection_name=collection_name,
        documents=["Dog", "Chair"],
        metadatas=[{"source": "my_source"}, {"source": "my_source"}],
        ids=["id1", "id2"]
    )

    results = memory_vector_db.query(
        collection_name=collection_name,
        query_texts=["Animal"],
        n_results=1
    )

    assert results["ids"] == [['id1']]


@pytest.mark.asyncio
async def test_query_service_add(memory_vector_db):
    collection_name = "test_collection"
    user_email = "testuser@somemail.com"
    project_id = "ID1234"

    vector_service = VectorService(vector_db=memory_vector_db, collection_name=collection_name)
    vector_service.add_vector_to_project(
        user_email=user_email,
        project_id=project_id,
        documents=["Dog", "Chair"],
        ids=["id1", "id2"]
    )

    result = vector_service.query_vector_from_project(
        user_email=user_email,
        project_id=project_id,
        query_texts=["Animal"],
        n_results=1
    )

    assert result["ids"] == [['id1']]


@pytest.mark.asyncio
async def test_query_service_multiple_users(memory_vector_db):
    collection_name = "test_collection"
    my_user_email = "my_user@someuser.com"
    other_user_email = "other_user@somemail.com"
    project_id = "ID1234"

    vector_service = VectorService(vector_db=memory_vector_db, collection_name=collection_name)
    vector_service.add_vector_to_project(
        user_email=other_user_email,
        project_id=project_id,
        documents=["Dog", "Chair"],
        ids=["id1", "id2"]
    )

    result = vector_service.query_vector_from_project(
        user_email=my_user_email,
        project_id=project_id,
        query_texts=["Animal"],
        n_results=1
    )

    assert result["ids"] == [[]]

    vector_service.add_vector_to_project(
        user_email=my_user_email,
        project_id=project_id,
        documents=["Dog", "Chair"],
        ids=["id3", "id4"]
    )

    result = vector_service.query_vector_from_project(
        user_email=my_user_email,
        project_id=project_id,
        query_texts=["Animal"],
        n_results=1
    )

    assert result["ids"] == [['id3']]


@pytest.mark.asyncio
async def test_add_two_collections_then_correctly_list_all_added_collections(memory_vector_db):
    collection1_vector_service = VectorService(vector_db=memory_vector_db, collection_name="collection1")
    collection2_vector_service = VectorService(vector_db=memory_vector_db, collection_name="collection2")

    listed_collections = collection1_vector_service.list_collections()
    assert set(listed_collections) == {"collection1", "collection2"}


