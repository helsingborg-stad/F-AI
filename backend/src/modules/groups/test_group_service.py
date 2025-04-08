import pytest

from src.modules.groups.protocols.IGroupService import IGroupService


class BaseGroupServiceTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_group(service: IGroupService):
        group_id = await service.create_group(
            'me@example.com',
            'test group',
            ['john@example.com', 'jane@example.com'],
            ['test.write', 'test.read'],
            resources=['resource_a', 'resource_b']
        )

        group = await service.get_group_by_id('me@example.com', group_id)

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
        assert len(group.resources) == 2
        assert 'resource_a' in group.resources
        assert 'resource_b' in group.resources

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_group_force_id(service: IGroupService):
        group_id = await service.create_group(
            'me@example.com',
            'test group',
            ['john@example.com', 'jane@example.com'],
            ['test.write', 'test.read'],
            # TODO: this currently relies on the ID being Mongo-compatible (ObjectId) - ideally it should not have to
            force_id='ff00000000000000000000ff',
            resources=[]
        )

        group = await service.get_group_by_id('me@example.com', group_id)

        assert group
        assert group.id == 'ff00000000000000000000ff'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_group_by_id_invalid_uid(service: IGroupService):
        group_id = await service.create_group(
            'me@example.com',
            'test group',
            ['john@example.com', 'jane@example.com'],
            ['test.write', 'test.read'],
            resources=['resource_a', 'resource_b']
        )

        group = await service.get_group_by_id(as_uid='jane@example.com', group_id=group_id)

        assert group is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_group_by_id_invalid_id(service: IGroupService):
        result = await service.get_group_by_id('', 'invalid')

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_owned_groups(service: IGroupService):
        group1 = await service.create_group('john', '1', ['john'], ['x'], ['a'])
        group2 = await service.create_group('john', '2', ['jane'], ['y'], ['b'])
        ______ = await service.create_group('jane', '3', ['jane'], ['z'], ['c'])
        ______ = await service.create_group('pete', '4', ['john'], ['w'], ['d'])

        groups = await service.get_owned_groups(as_uid='john')
        result1 = next((g for g in groups if g.id == group1), None)
        result2 = next((g for g in groups if g.id == group2), None)

        assert len(groups) == 2
        assert result1 is not None
        assert result1.owner == 'john'
        assert result1.label == '1'
        assert result1.members == ['john']
        assert result1.scopes == ['x']
        assert result1.resources == ['a']
        assert result2 is not None
        assert result2.owner == 'john'
        assert result2.label == '2'
        assert result2.members == ['jane']
        assert result2.scopes == ['y']
        assert result2.resources == ['b']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_groups_by_member(service: IGroupService):
        group1 = await service.create_group('john', '1', ['john'], ['x'], ['a'])
        ______ = await service.create_group('john', '2', ['jane'], ['y'], ['b'])
        ______ = await service.create_group('jane', '3', ['jane'], ['z'], ['c'])
        group2 = await service.create_group('pete', '4', ['john'], ['w'], ['d'])

        groups = await service.get_groups_by_member(member='john')
        result1 = next((g for g in groups if g.id == group1), None)
        result2 = next((g for g in groups if g.id == group2), None)

        assert len(groups) == 2
        assert result1 is not None
        assert result1.owner == 'john'
        assert result1.label == '1'
        assert result1.members == ['john']
        assert result1.scopes == ['x']
        assert result1.resources == ['a']
        assert result2 is not None
        assert result2.owner == 'pete'
        assert result2.label == '4'
        assert result2.members == ['john']
        assert result2.scopes == ['w']
        assert result2.resources == ['d']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_groups_wildcard(service: IGroupService):
        group1 = await service.create_group('jane', '1', ['*@*'], ['x'], ['a'])
        group2 = await service.create_group('jane', '2', ['*@example.com'], ['y'], ['b'])
        group3 = await service.create_group('john', '3', ['john@*'], ['z'], ['c'])
        ______ = await service.create_group('john', '4', ['*@example.se'], ['w'], ['d'])

        groups = await service.get_groups_by_member(member='john@example.com')

        result1 = next((g for g in groups if g.id == group1), None)
        result2 = next((g for g in groups if g.id == group2), None)
        result3 = next((g for g in groups if g.id == group3), None)

        assert len(groups) == 3
        assert result1 is not None
        assert result1.owner == 'jane'
        assert result1.label == '1'
        assert result1.scopes == ['x']
        assert result1.resources == ['a']
        assert result2 is not None
        assert result2.owner == 'jane'
        assert result2.label == '2'
        assert result2.scopes == ['y']
        assert result2.resources == ['b']
        assert result3 is not None
        assert result3.owner == 'john'
        assert result3.label == '3'
        assert result3.scopes == ['z']
        assert result3.resources == ['c']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_members(service: IGroupService):
        group_id = await service.create_group('john', '1', [], ['x'], ['a'])

        success = await service.set_group_members(as_uid='john', group_id=group_id, members=['john'])
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success is True
        assert result.id == group_id
        assert result.members == ['john']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_members_twice(service: IGroupService):
        group_id = await service.create_group('john', '1', [], ['x'], ['a'])

        success1 = await service.set_group_members(as_uid='john', group_id=group_id, members=['john'])
        success2 = await service.set_group_members(as_uid='john', group_id=group_id, members=['jane', 'pete'])
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success1 is True
        assert success2 is True
        assert result.members == ['jane', 'pete']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_members_invalid_uid(service: IGroupService):
        group_id = await service.create_group('john', '1', ['jane'], ['x'], ['a'])

        success = await service.set_group_members(as_uid='pete', group_id=group_id, members=['emma'])
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success is False
        assert result.id == group_id
        assert result.members == ['jane']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_members_invalid_id(service: IGroupService):
        success = await service.set_group_members(as_uid='john', group_id='does not exist', members=['john'])
        result = await service.get_group_by_id(as_uid='john', group_id='does not exist')

        assert success is False
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_scopes(service: IGroupService):
        group_id = await service.create_group('john', '1', [], ['x'], [])

        success = await service.set_group_scopes(as_uid='john', group_id=group_id, scopes=['y', 'z'])
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success is True
        assert result.scopes == ['y', 'z']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_scopes_invalid_uid(service: IGroupService):
        group_id = await service.create_group('john', '1', [], ['x'], [])

        success = await service.set_group_scopes(as_uid='jane', group_id=group_id, scopes=['y', 'z'])
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success is False
        assert result.scopes == ['x']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_group_scopes_invalid_id(service: IGroupService):
        success = await service.set_group_scopes(as_uid='john', group_id='does not exist', scopes=['y', 'z'])

        result = await service.get_group_by_id(as_uid='john', group_id='does not exist')

        assert success is False
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_group_resource(service: IGroupService):
        group_id = await service.create_group('john', '1', [], [], ['a'])

        success1 = await service.add_group_resource(as_uid='john', group_id=group_id, resource='a')
        success2 = await service.add_group_resource(as_uid='john', group_id=group_id, resource='b')
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success1 is True
        assert success2 is True
        assert result.resources == ['a', 'b']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_group_resource_invalid_uid(service: IGroupService):
        group_id = await service.create_group('john', '1', [], [], ['a'])

        success = await service.add_group_resource(as_uid='jane', group_id=group_id, resource='b')
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success is False
        assert result.resources == ['a']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_add_group_resource_invalid_id(service: IGroupService):
        success = await service.add_group_resource(as_uid='john', group_id='does not exist', resource='a')

        result = await service.get_group_by_id(as_uid='john', group_id='does not exist')

        assert success is False
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_remove_group_resource(service: IGroupService):
        group_id = await service.create_group('john', '1', [], ['x'], ['a', 'b'])

        success1 = await service.remove_group_resource(as_uid='john', group_id=group_id, resource='a')
        success2 = await service.remove_group_resource(as_uid='john', group_id=group_id, resource='c')
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success1 is True
        assert success2 is True
        assert result.resources == ['b']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_remove_group_resource_invalid_uid(service: IGroupService):
        group_id = await service.create_group('john', '1', [], ['x'], ['a', 'b'])

        success = await service.remove_group_resource(as_uid='jane', group_id=group_id, resource='a')
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert success is False
        assert result.resources == ['a', 'b']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_remove_group_resource_invalid_id(service: IGroupService):
        success = await service.remove_group_resource(as_uid='john', group_id='does not exist', resource='a')

        result = await service.get_group_by_id(as_uid='john', group_id='does not exist')

        assert success is False
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_group(service: IGroupService):
        group_id = await service.create_group('john', '1', [], [], [])

        await service.delete_group(as_uid='john', group_id=group_id)
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_group_invalid_uid(service: IGroupService):
        group_id = await service.create_group('john', '1', [], [], [])

        await service.delete_group(as_uid='jane', group_id=group_id)
        result = await service.get_group_by_id(as_uid='john', group_id=group_id)

        assert result.id == group_id

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_group_invalid_id(service: IGroupService):
        await service.delete_group(as_uid='john', group_id='does not exist')

        result = await service.get_group_by_id('john', 'does not exist')

        assert result is None
