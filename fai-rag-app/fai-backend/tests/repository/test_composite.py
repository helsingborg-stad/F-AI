import pytest
from pydantic import BaseModel

from fai_backend.repository.composite import CompositeRepo
from fai_backend.repository.memory import InMemoryRepo


class Item(BaseModel):
    id: str = ''
    name: str
    value: int


@pytest.fixture
def memory_repo():
    return InMemoryRepo[Item]()


@pytest.fixture
def composite_repo(memory_repo):
    return CompositeRepo[Item]([memory_repo])


@pytest.mark.parametrize('item', [Item(name='TestItem', value=10)])
@pytest.mark.asyncio
async def test_composite_create_and_get_item(composite_repo, item):
    created_item = await composite_repo.create(item)

    assert created_item.id is not None
    assert created_item.name == 'TestItem'
    assert created_item.value == 10

    retrieved_item = await composite_repo.get(created_item.id)
    assert retrieved_item == created_item


@pytest.mark.parametrize(
    'items_to_create', [[Item(name=f'Item{i}', value=i) for i in range(5)]]
)
@pytest.mark.asyncio
async def test_composite_list_items(composite_repo, items_to_create):
    for item in items_to_create:
        await composite_repo.create(item)

    listed_items = await composite_repo.list()
    assert len(listed_items) == 5
    assert listed_items == items_to_create


@pytest.mark.parametrize(
    'item, updated_data',
    [(Item(name='OldItem', value=15), {'name': 'NewItem', 'value': 20})],
)
@pytest.mark.asyncio
async def test_composite_update_item_by_object(composite_repo, item, updated_data):
    created_item = await composite_repo.create(item)

    created_item.name = updated_data.get('name')
    created_item.value = updated_data.get('value')

    updated_item = await composite_repo.update(created_item)
    assert updated_item.name == updated_data.get('name')
    assert updated_item.value == updated_data.get('value')


@pytest.mark.parametrize(
    'item, updated_data',
    [(Item(name='OldItem', value=15), {'name': 'NewItem', 'value': 20})],
)
@pytest.mark.asyncio
async def test_composite_update_item_by_id(composite_repo, item, updated_data):
    created_item = await composite_repo.create(item)

    updated_item = await composite_repo.update_id(created_item.id, updated_data)
    assert updated_item.name == 'NewItem'
    assert updated_item.value == 20


@pytest.mark.parametrize('item', [Item(name='ToDelete', value=25)])
@pytest.mark.asyncio
async def test_composite_delete_item(composite_repo, item):
    created_item = await composite_repo.create(item)

    deleted_item = await composite_repo.delete(created_item.id)
    assert deleted_item == created_item

    retrieved_item = await composite_repo.get(created_item.id)
    assert retrieved_item is None


@pytest.mark.parametrize('non_existent_id', ['999'])
@pytest.mark.asyncio
async def test_composite_non_existent_item(composite_repo, non_existent_id):
    retrieved_item = await composite_repo.get(non_existent_id)
    assert retrieved_item is None

    updated_item = await composite_repo.update_id(non_existent_id, {'name': 'NoItem'})
    assert updated_item is None

    deleted_item = await composite_repo.delete(non_existent_id)
    assert deleted_item is None
