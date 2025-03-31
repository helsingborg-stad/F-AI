import pytest

from src.modules.groups.protocols.IGroupService import IGroupService


class BaseGroupServiceTestClass:

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_group_by_id(service: IGroupService):
        group_id = await service.create_group(
            'me@example.com',
            'test group',
            ['john@example.com', 'jane@example.com'],
            ['test.write', 'test.read']
        )

        group = await service.get_group_by_id(group_id)

        assert group
        assert group.id == group_id
        assert group.label == 'test group'
        assert group.owner == 'me@example.com'
        assert len(group.members) == 2
        assert 'john@example.com' in group.members
        assert 'jane@example.com' in group.members
        assert len(group.scopes) == 2
        assert 'test.write' in group.scopes
        assert 'test.read' in group.scopes

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_force_id(service: IGroupService):
        group_id = await service.create_group(
            'me@example.com',
            'test group',
            ['john@example.com', 'jane@example.com'],
            ['test.write', 'test.read'],
            force_id='ff00000000000000000000ff'
        )

        group = await service.get_group_by_id(group_id)

        assert group
        assert group.id == 'ff00000000000000000000ff'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_group_by_id_invalid(service: IGroupService):
        result = await service.get_group_by_id('invalid')

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_groups(service: IGroupService):
        group1 = await service.create_group(
            'john@example.com',
            "john's group",
            ['john.jr@example.com'],
            ['test.read']
        )
        group2 = await service.create_group(
            'jane@example.com',
            "jane's group",
            ['jane.jr@example.com'],
            ['test.write']
        )

        result = await service.get_groups()
        result1 = next((g for g in result if g.id == group1), None)
        result2 = next((g for g in result if g.id == group2), None)

        assert len(result) == 2
        assert result1
        assert result2
        assert result1.owner == 'john@example.com'
        assert result1.label == "john's group"
        assert result1.members == ['john.jr@example.com']
        assert result1.scopes == ['test.read']
        assert result2.owner == 'jane@example.com'
        assert result2.label == "jane's group"
        assert result2.members == ['jane.jr@example.com']
        assert result2.scopes == ['test.write']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_groups_by_member(service: IGroupService):
        group1 = await service.create_group(owner='a', label='a', scopes=['a'], members=['john'])
        group2 = await service.create_group(owner='b', label='b', scopes=['b'], members=['jane', 'john'])
        group3 = await service.create_group(owner='c', label='c', scopes=['c'], members=['jane'])

        result = await service.get_groups_by_member('john')

        assert len(result) == 2
        assert group1 in [g.id for g in result]
        assert group2 in [g.id for g in result]

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_groups_by_member_invalid(service: IGroupService):
        result = await service.get_groups_by_member('invalid')

        assert len(result) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_members(service: IGroupService):
        group = await service.create_group(owner='a', label='a', scopes=['a'], members=['bob'])

        await service.set_group_members(group, ['john', 'jane'])
        result = await service.get_group_by_id(group)

        assert result.members == ['john', 'jane']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_members_invalid(service: IGroupService):
        await service.set_group_members('invalid group', ['bob'])

        result = await service.get_group_by_id('invalid group')

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_scopes(service: IGroupService):
        group = await service.create_group(owner='a', label='a', scopes=['a', 'b'], members=['john'])

        await service.set_group_scopes(group, ['c'])
        result = await service.get_group_by_id(group)

        assert result.scopes == ['c']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_scopes_invalid(service: IGroupService):
        await service.set_group_scopes('invalid group', ['c'])

        result = await service.get_group_by_id('invalid group')

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_group(service: IGroupService):
        group = await service.create_group(owner='a', label='a', scopes=['a'], members=['john'])

        await service.delete_group(group)
        result = await service.get_group_by_id(group)

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_group_invalid(service: IGroupService):
        await service.delete_group('invalid group')
        result = await service.get_group_by_id('invalid group')

        assert result is None
