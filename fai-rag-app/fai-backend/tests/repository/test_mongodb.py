import pytest
import pytest_asyncio
from beanie import Document, init_beanie
from bson import ObjectId
from mongomock_motor import AsyncMongoMockClient

from fai_backend.repository.mongodb import MongoDBRepo


class SampleDocument(Document):
    name: str
    age: int

    class Settings:
        use_state_management = True


@pytest_asyncio.fixture
async def mongo_repo():
    client = AsyncMongoMockClient()
    db = client.test_db
    await init_beanie(database=db, document_models=[SampleDocument])
    yield MongoDBRepo(SampleDocument)
    await SampleDocument.get_motor_collection().drop()


@pytest.mark.asyncio
async def test_list(mongo_repo):
    await SampleDocument(name='Alice', age=30).insert()
    await SampleDocument(name='Bob', age=25).insert()

    documents = await mongo_repo.list()

    assert len(documents) == 2
    assert documents[0].name == 'Alice'
    assert documents[1].name == 'Bob'


@pytest.mark.asyncio
async def test_create(mongo_repo):
    new_document = SampleDocument(name='Charlie', age=40)

    created_document = await mongo_repo.create(new_document)

    assert created_document.name == 'Charlie'
    assert created_document.age == 40
    assert created_document.id is not None


@pytest.mark.asyncio
async def test_get_existing_document(mongo_repo):
    sample_document = await SampleDocument(name='Dave', age=35).insert()

    retrieved_document = await mongo_repo.get(str(sample_document.id))

    assert retrieved_document is not None
    assert retrieved_document.name == 'Dave'
    assert retrieved_document.age == 35


@pytest.mark.asyncio
async def test_get_non_existing_document(mongo_repo):
    retrieved_document = await mongo_repo.get(str(ObjectId()))

    assert retrieved_document is None


@pytest.mark.asyncio
async def test_update_existing_document(mongo_repo):
    sample_document = await SampleDocument(name='Eve', age=45).insert()

    updated_document = await mongo_repo.update(
        str(sample_document.id), {'name': 'Eve Updated', 'age': 50}
    )

    assert updated_document is not None
    assert updated_document.name == 'Eve Updated'
    assert updated_document.age == 50


@pytest.mark.asyncio
async def test_update_non_existing_document(mongo_repo):
    updated_document = await mongo_repo.update(
        str(ObjectId()), {'name': 'Non Existing', 'age': 99}
    )

    assert updated_document is None


@pytest.mark.asyncio
async def test_delete_existing_document(mongo_repo):
    sample_document = await SampleDocument(name='Frank', age=55).insert()
    deleted_document = await mongo_repo.delete(str(sample_document.id))

    assert deleted_document is not None
    assert deleted_document.name == 'Frank'
    assert deleted_document.age == 55

    assert await SampleDocument.get(sample_document.id) is None


@pytest.mark.asyncio
async def test_delete_non_existing_document(mongo_repo):
    deleted_document = await mongo_repo.delete(str(ObjectId()))

    assert deleted_document is None
