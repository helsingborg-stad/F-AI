import pytest
import pytest_asyncio
from beanie import Document, init_beanie
from bson import ObjectId
from mongomock_motor import AsyncMongoMockClient
from pydantic import BaseModel, Field

from fai_backend.repository.mongodb import MongoDBRepo
from fai_backend.repository.query.component import AttributeAssignment, AttributeComparison, LogicalExpression


class Employee(BaseModel):
    id: ObjectId = Field(alias='_id', default_factory=ObjectId)
    name: str
    age: int
    perks: list[str] = []

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True


class EmployeeDocument(Document, Employee):
    class Settings:
        use_state_management = True


@pytest_asyncio.fixture
async def mongo_repo():
    await init_beanie(database=(AsyncMongoMockClient()).test_db, document_models=[EmployeeDocument])
    yield MongoDBRepo[Employee, EmployeeDocument](Employee, EmployeeDocument)
    await EmployeeDocument.get_motor_collection().drop()


@pytest.mark.asyncio
async def test_list(mongo_repo):
    await mongo_repo.create(Employee(name='Alice', age=30))
    await mongo_repo.create(Employee(name='Bob', age=25))

    documents = await mongo_repo.list(None)

    assert len(documents) == 2
    assert documents[0].name == 'Alice'
    assert documents[1].name == 'Bob'


@pytest.mark.asyncio
async def test_create(mongo_repo):
    created_document = await mongo_repo.create(Employee(name='Charlie', age=40))
    assert created_document.name == 'Charlie'
    assert created_document.age == 40
    assert created_document.id is not None


@pytest.mark.asyncio
async def test_get_existing_document(mongo_repo):
    sample_document = await mongo_repo.create(Employee(name='Dave', age=35))

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
    created = await mongo_repo.create(Employee(name='Eve', age=45))
    document = await mongo_repo.get(created.id)
    saved_id = document.id
    updated_document = await mongo_repo.update(
        document.copy(update={'name': 'Eve Updated', 'age': 50})
    )

    assert updated_document is not None
    assert updated_document.name == 'Eve Updated'
    assert updated_document.age == 50
    assert updated_document.id == saved_id


@pytest.mark.asyncio
async def test_update_non_existing_document(mongo_repo):
    with pytest.raises(AttributeError) as exception_info:
        await mongo_repo.update(
            Employee(name='Non Existing', age=99)
        )

    assert "'Employee' object has no attribute 'save_changes'" in str(exception_info.value)


@pytest.mark.asyncio
async def test_delete_existing_document(mongo_repo):
    sample_document = await mongo_repo.create(Employee(name='Frank', age=55))
    deleted_document = await mongo_repo.delete(str(sample_document.id))

    assert deleted_document is not None
    assert deleted_document.name == 'Frank'
    assert deleted_document.age == 55

    assert await mongo_repo.get(sample_document.id) is None


@pytest.mark.asyncio
async def test_delete_non_existing_document(mongo_repo):
    deleted_document = await mongo_repo.delete(str(ObjectId()))

    assert deleted_document is None


@pytest.mark.asyncio
async def test_sort_by_age_descending(mongo_repo):
    await mongo_repo.create(Employee(name='Bob', age=25))
    await mongo_repo.create(Employee(name='Alice', age=30))
    await mongo_repo.create(Employee(name='James', age=40))

    documents = await mongo_repo.list(None, sort_by='age', sort_order='desc')

    assert len(documents) == 3
    assert documents[0].name == 'James'
    assert documents[1].name == 'Alice'
    assert documents[2].name == 'Bob'


@pytest.mark.asyncio
async def test_sort_by_age_ascending(mongo_repo):
    await mongo_repo.create(Employee(name='Alice', age=30))
    await mongo_repo.create(Employee(name='Bob', age=25))
    await mongo_repo.create(Employee(name='Liz', age=16))

    documents = await mongo_repo.list(None, sort_by='age', sort_order='asc')

    assert len(documents) == 3
    assert documents[0].name == 'Liz'
    assert documents[1].name == 'Bob'
    assert documents[2].name == 'Alice'


@pytest.mark.asyncio
async def test_list_by_age_in_range(mongo_repo):
    await mongo_repo.create(Employee(name='Carl', age=40))
    await mongo_repo.create(Employee(name='Alice', age=29))
    await mongo_repo.create(Employee(name='Bob', age=25))
    await mongo_repo.create(Employee(name='Liz', age=16))

    documents = await mongo_repo.list(LogicalExpression('AND', [
        AttributeComparison('age', '>=', 20),
        AttributeComparison('age', '<=', 30)
    ]), sort_by='age', sort_order='desc')

    assert len(documents) == 2
    assert documents[0].name == 'Alice'
    assert documents[1].name == 'Bob'


@pytest.mark.asyncio
async def test_query_with_attribute_assignment_expression(mongo_repo):
    await mongo_repo.create(Employee(name='Alice', age=30, perks=['Health Insurance']))
    await mongo_repo.create(Employee(name='Bob', age=25, perks=['Dental Insurance']))
    await mongo_repo.create(Employee(name='Charlie', age=35, perks=['Health Insurance', 'Dental Insurance']))
    await mongo_repo.create(Employee(name='David', age=40, perks=['Vision Insurance']))
    documents = await mongo_repo.list(
        AttributeAssignment('perks', 'Health Insurance'),
        sort_by='age', sort_order='desc'
    )

    assert len(documents) == 2
    assert documents[0].name == 'Charlie'
    assert documents[1].name == 'Alice'
