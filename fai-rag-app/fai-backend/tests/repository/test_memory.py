import pytest
from pydantic import BaseModel

from fai_backend.repository.memory import InMemoryRepo


class Item(BaseModel):
    id: str = ''
    name: str
    value: int


@pytest.fixture
def repo():
    return InMemoryRepo[Item]()


@pytest.mark.parametrize('item', [Item(name='TestItem', value=10)])
@pytest.mark.asyncio
async def test_create_and_get_item(repo, item):
    created_item = await repo.create(item)

    assert created_item.id is not None
    assert created_item.name == 'TestItem'
    assert created_item.value == 10

    retrieved_item = await repo.get(created_item.id)
    assert retrieved_item == created_item


@pytest.mark.parametrize(
    'items_to_create', [[Item(name=f'Item{i}', value=i) for i in range(5)]]
)
@pytest.mark.asyncio
async def test_list_items(repo, items_to_create):
    for item in items_to_create:
        await repo.create(item)

    listed_items = await repo.list()
    assert len(listed_items) == 5
    assert listed_items == items_to_create


@pytest.mark.parametrize(
    'item, updated_data',
    [(Item(name='OldItem', value=15), {'name': 'NewItem', 'value': 20})],
)
@pytest.mark.asyncio
async def test_update_item(repo, item, updated_data):
    created_item = await repo.create(item)

    updated_item = await repo.update_id(created_item.id, updated_data)
    assert updated_item.name == 'NewItem'
    assert updated_item.value == 20


@pytest.mark.parametrize('item', [Item(name='ToDelete', value=25)])
@pytest.mark.asyncio
async def test_delete_item(repo, item):
    created_item = await repo.create(item)

    deleted_item = await repo.delete(created_item.id)
    assert deleted_item == created_item

    retrieved_item = await repo.get(created_item.id)
    assert retrieved_item is None


@pytest.mark.parametrize('non_existent_id', ['999'])
@pytest.mark.asyncio
async def test_non_existent_item(repo, non_existent_id):
    retrieved_item = await repo.get(non_existent_id)
    assert retrieved_item is None

    updated_item = await repo.update_id(non_existent_id, {'name': 'NoItem'})
    assert updated_item is None

    deleted_item = await repo.delete(non_existent_id)
    assert deleted_item is None
