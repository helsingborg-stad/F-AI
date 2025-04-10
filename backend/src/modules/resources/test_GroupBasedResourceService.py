import pytest
import pytest_asyncio
from pymongo.asynchronous.database import AsyncDatabase

from src.modules.groups.MongoGroupService import MongoGroupService
from src.modules.groups.protocols.IGroupService import IGroupService
from src.modules.resources.GroupBasedResourceService import GroupBasedResourceService
from src.modules.resources.protocols.IResourceService import IResourceService


@pytest_asyncio.fixture
def group_service(mongo_test_db: AsyncDatabase):
    yield MongoGroupService(mongo_test_db)


@pytest_asyncio.fixture
def resource_service(group_service: IGroupService):
    return GroupBasedResourceService(group_service)


class TestGroupBasedResourceService:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_resources(group_service: IGroupService, resource_service: IResourceService):
        await group_service.create_group(
            as_uid='',
            label='',
            scopes=[],
            members=['john@example.com'],
            resources=['resource_a', 'resource_b']
        )

        await group_service.create_group(
            as_uid='',
            label='excluded',
            scopes=[],
            members=['john@example.com'],
            resources=['resource_b', 'resource_c']
        )

        await group_service.create_group(
            as_uid='',
            label='excluded',
            scopes=[],
            members=['*@*'],
            resources=['resource_d']
        )

        result = await resource_service.get_resources(as_uid='john@example.com')

        assert len(result) == 4
        assert 'resource_a' in result
        assert 'resource_b' in result
        assert 'resource_c' in result
        assert 'resource_d' in result

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_filter_accessible_resources(group_service: IGroupService, resource_service: IResourceService):
        await group_service.create_group(
            as_uid='',
            label='',
            scopes=[],
            members=['john@example.com'],
            resources=['resource_a']
        )

        await group_service.create_group(
            as_uid='',
            label='excluded',
            scopes=[],
            members=['jane@example.com'],
            resources=['resource_b', 'resource_a']
        )

        result = await resource_service.filter_accessible_resources(
            as_uid='john@example.com',
            resources=['resource_b', 'resource_a']
        )

        assert result == ['resource_a']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_group_filter_accessible_resources_invalid_uid(group_service: IGroupService,
                                                                 resource_service: IResourceService):
        result = await resource_service.filter_accessible_resources(
            as_uid='does not exist',
            resources=['resource_b', 'resource_a']
        )

        assert len(result) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_group_filter_accessible_resources_no_resources(group_service: IGroupService,
                                                                  resource_service: IResourceService):
        await group_service.create_group(
            as_uid='',
            label='',
            scopes=[],
            members=['john@example.com'],
            resources=['resource_a']
        )

        result = await resource_service.filter_accessible_resources(
            as_uid='does not exist',
            resources=['resource_b']
        )

        assert len(result) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_can_access(group_service: IGroupService, resource_service: IResourceService):
        await group_service.create_group(
            as_uid='',
            label='',
            scopes=[],
            members=['john@example.com'],
            resources=['resource_a']
        )

        result1 = await resource_service.can_access(as_uid='john@example.com', resource='resource_a')
        result2 = await resource_service.can_access(as_uid='john@example.com', resource='resource_b')

        assert result1 is True
        assert result2 is False
