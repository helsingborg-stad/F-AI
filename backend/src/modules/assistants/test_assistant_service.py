import pytest

from src.modules.assistants.models.Model import Model
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.groups.protocols.IGroupService import IGroupService


async def _create_mock_group(group_service: IGroupService, resource: str):
    await group_service.create_group(
        as_uid='john',
        label='MOCK',
        members=['john', 'jane'],
        scopes=[],
        resources=[resource]
    )


class BaseAssistantServiceTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_get_assistant(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert len(aid) > 0
        assert result is not None
        assert result.id == aid
        assert result.owner == 'john'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_available_models(service: IAssistantService):
        success = await service.set_available_models(models=[
            Model(key='a', provider='A', display_name='Cool Model A', description='cool model A'),
            Model(key='b', provider='B', display_name='Cool Model B', description='cool model B'),
        ])

        result = await service.get_available_models(as_uid='john')

        assert success is True
        assert len(result) == 2
        assert result[0].key == 'a'
        assert result[0].provider == 'A'
        assert result[0].display_name == 'Cool Model A'
        assert result[0].description == 'cool model A'
        assert result[1].key == 'b'
        assert result[1].provider == 'B'
        assert result[1].display_name == 'Cool Model B'
        assert result[1].description == 'cool model B'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_available_models_override(service: IAssistantService):
        success1 = await service.set_available_models(models=[
            Model(key='a', provider='A', display_name='Cool Model A', description='my cool model A'),
            Model(key='b', provider='B', display_name='Cool Model B', description='my cool model B'),
        ])
        success2 = await service.set_available_models(models=[
            Model(key='c', provider='C', display_name='Cool Model C', description='my cool model C'),
        ])

        result = await service.get_available_models(as_uid='john')

        assert success1 is True
        assert success2 is True
        assert len(result) == 1
        assert result[0].key == 'c'
        assert result[0].provider == 'C'
        assert result[0].display_name == 'Cool Model C'
        assert result[0].description == 'my cool model C'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_available_models_twice(service: IAssistantService):
        success1 = await service.set_available_models(models=[])
        success2 = await service.set_available_models(models=[])

        assert success1 is True
        assert success2 is True

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistant_key_redacted(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')
        await service.update_assistant(as_uid='john', assistant_id=aid, llm_api_key='my_secret_key')

        result1 = await service.get_assistant(as_uid='john', assistant_id=aid)
        result2 = await service.get_assistant(as_uid='john', assistant_id=aid, redact_key=False)
        result3 = await service.get_owned_assistants(as_uid='john')

        assert 'my_secret_key' not in result1.llm_api_key
        assert 'my_secret_key' in result2.llm_api_key
        assert 'my_secret_key' not in result3[0].llm_api_key

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistant_invalid_uid(service: IAssistantService):
        aid = await service.create_assistant(as_uid='emma')

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistant_invalid_assistant_id(service: IAssistantService):
        result = await service.get_assistant(as_uid='john', assistant_id='does not exist')

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistant_group(service: IAssistantService, group_service: IGroupService):
        aid = await service.create_assistant(as_uid='john')
        await _create_mock_group(group_service, aid)

        result_same_group = await service.get_assistant(as_uid='jane', assistant_id=aid)
        result_not_same_group = await service.get_assistant(as_uid='pete', assistant_id=aid)

        assert result_same_group is not None
        assert result_same_group.id == aid
        assert result_not_same_group is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_owned_assistants(service: IAssistantService):
        aid1 = await service.create_assistant(as_uid='john')
        aid2 = await service.create_assistant(as_uid='john')
        aid3 = await service.create_assistant(as_uid='jane')

        result = await service.get_owned_assistants(as_uid='john')

        assert len(result) == 2
        assert aid1 in [a.id for a in result]
        assert next(a for a in result if a.id == aid1).owner == 'john'
        assert aid2 in [a.id for a in result]
        assert next(a for a in result if a.id == aid2).owner == 'john'
        assert aid3 not in [a.id for a in result]

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_available_assistants(service: IAssistantService, group_service: IGroupService):
        john_private_aid = await service.create_assistant(as_uid='john')
        shared_aid = await service.create_assistant(as_uid='john')
        jane_private_aid = await service.create_assistant(as_uid='jane')
        await _create_mock_group(group_service, shared_aid)

        result = await service.get_available_assistants(as_uid='jane')

        assert len(result) == 2
        assert jane_private_aid in [a.id for a in result]
        assert next(a for a in result if a.id == jane_private_aid).owner == 'jane'
        assert shared_aid in [a.id for a in result]
        assert next(a for a in result if a.id == shared_aid).owner == 'john'
        assert john_private_aid not in [a.id for a in result]

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_basic(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        success = await service.update_assistant(as_uid='john', assistant_id=aid, name='test assistant',
                                                 description='test description')

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert success is True
        assert result.meta.name == 'test assistant'
        assert result.meta.description == 'test description'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_consecutive(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        success1 = await service.update_assistant(as_uid='john', assistant_id=aid, name='test assistant')
        success2 = await service.update_assistant(as_uid='john', assistant_id=aid, sample_questions=['hello', 'world'])
        success3 = await service.update_assistant(as_uid='john', assistant_id=aid, name='my cool assistant')

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert success1 is True
        assert success2 is True
        assert success3 is True
        assert result.meta.name == 'my cool assistant'
        assert result.meta.sample_questions == ['hello', 'world']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_full(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        success = await service.update_assistant(
            as_uid='john',
            assistant_id=aid,
            name='a',
            description='b',
            allow_files=True,
            sample_questions=['c', 'd', 'e'],
            model='f',
            llm_api_key='g',
            instructions='h',
            temperature=3.1415,
            max_tokens=1337,
            collection_id='i',
        )

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert success is True
        assert result.id == aid
        assert result.owner == 'john'
        assert result.meta.name == 'a'
        assert result.meta.description == 'b'
        assert result.meta.allow_files is True
        assert result.meta.sample_questions == ['c', 'd', 'e']
        assert result.model == 'f'
        assert result.instructions == 'h'
        assert result.temperature == 3.1415
        assert result.max_tokens == 1337
        assert result.collection_id == 'i'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_invalid_uid(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        success = await service.update_assistant(as_uid='jane', assistant_id=aid, name='evil override')
        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert success is False
        assert result.meta.name != 'evil override'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_invalid_assistant_id(service: IAssistantService):
        success = await service.update_assistant(as_uid='john', assistant_id='invalid', name='hello')
        result = await service.get_assistant(as_uid='john', assistant_id='invalid')

        assert success is False
        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_assistant(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        await service.delete_assistant(as_uid='john', assistant_id=aid)
        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_assistant_invalid_uid(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        await service.delete_assistant(as_uid='jane', assistant_id=aid)
        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert result is not None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_assistant_invalid_assistant_id(service: IAssistantService):
        await service.delete_assistant(as_uid='john', assistant_id='invalid')
        assert True
