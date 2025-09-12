import pytest

from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.groups.protocols.IGroupService import IGroupService


async def _create_mock_group(group_service: IGroupService, resource: str, as_uid='john'):
    await group_service.create_group(
        as_uid=as_uid,
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
    async def test_create_assistant_force_id(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john', force_id='deadbeefbaadf00dcafe1234')

        assert aid == 'deadbeefbaadf00dcafe1234'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_important_defaults(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert isinstance(result.meta, dict)
        assert 'is_public' not in result.meta


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
    async def test_set_favorite(service: IAssistantService):
        aid1 = await service.create_assistant(as_uid='john')
        aid2 = await service.create_assistant(as_uid='john')
        aid3 = await service.create_assistant(as_uid='jane')

        result1 = await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid1)
        result2 = await service.get_favorite_assistants(as_uid='john')

        assert result1 is True
        assert len(result2) == 1
        assert result2[0].id == aid1

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_favorite_non_private_only(service: IAssistantService, group_service: IGroupService):
        aid1 = await service.create_assistant(as_uid='jane')
        aid2 = await service.create_assistant(as_uid='jane')
        aid3 = await service.create_assistant(as_uid='jane')
        aid4 = await service.create_assistant(as_uid='jane')

        await service.update_assistant(as_uid='jane', assistant_id=aid1, is_public=True)
        await service.update_assistant(as_uid='jane', assistant_id=aid3, is_public=True)
        await _create_mock_group(group_service, aid4, as_uid='jane')

        result1 = await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid1)
        result2 = await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid2)
        result3 = await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid3)
        result4 = await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid4)

        await service.update_assistant(as_uid='jane', assistant_id=aid3, is_public=False)

        result = await service.get_favorite_assistants(as_uid='john')

        assert result1 is True  # is public
        assert result2 is False  # was never public
        assert result3 is True  # was public at the time
        assert result4 is True  # shared via group

        assert len(result) == 2
        assert result[0].id == aid1
        assert result[1].id == aid4

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_favorite_twice(service: IAssistantService):
        aid1 = await service.create_assistant(as_uid='john')

        await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid1)
        await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid1)

        result = await service.get_favorite_assistants(as_uid='john')

        assert len(result) == 1
        assert result[0].id == aid1

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_remove_favorite(service: IAssistantService):
        aid1 = await service.create_assistant(as_uid='john')
        aid2 = await service.create_assistant(as_uid='john')

        await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid1)
        await service.set_assistant_as_favorite(as_uid='john', assistant_id=aid2)

        await service.remove_assistant_as_favorite(as_uid='john', assistant_id=aid1)
        result = await service.get_favorite_assistants(as_uid='john')

        assert len(result) == 1
        assert result[0].id == aid2

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistant_info(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')
        await service.update_assistant(
            as_uid='john',
            assistant_id=aid,
            model='fai:my_model',
            meta={
                'name': 'cool name',
                'description': 'cool desc',
                'avatar_base64': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==',
                'primary_color': '#facade',
                'sample_questions': ['a', 'b', 'c'],
            }
        )

        result = await service.get_assistant_info(as_uid='john', assistant_id=aid)

        assert result.id == aid
        assert result.model == 'fai:my_model'
        assert result.meta['name'] == 'cool name'
        assert result.meta['description'] == 'cool desc'
        assert result.meta[
                   'avatar_base64'] == 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=='
        assert result.meta['primary_color'] == '#facade'
        assert result.meta['sample_questions'] == ['a', 'b', 'c']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistant_info_public(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')
        await service.update_assistant(
            as_uid='john',
            assistant_id=aid,
            model='fai:my_model',
            is_public=True,
            meta={
                'name': 'cool name',
                'description': 'cool desc',
                'avatar_base64': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==',
                'primary_color': '#facade',
                'sample_questions': ['a', 'b', 'c'],
            }
        )
        private_aid = await service.create_assistant(as_uid='john')

        result1 = await service.get_assistant_info(as_uid='jane', assistant_id=aid)
        result2 = await service.get_assistant_info(as_uid='jane', assistant_id=private_aid)

        assert result1.id == aid
        assert result1.model == 'fai:my_model'
        assert result1.meta['name'] == 'cool name'
        assert result1.meta['description'] == 'cool desc'
        assert result1.meta[
                   'avatar_base64'] == 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=='
        assert result1.meta['primary_color'] == '#facade'
        assert result1.meta['sample_questions'] == ['a', 'b', 'c']

        assert result2 is None

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
        assert shared_aid in [a.id for a in result]
        assert john_private_aid not in [a.id for a in result]

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_available_assistants_completeness(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')
        await service.update_assistant(
            as_uid='john',
            assistant_id=aid,
            model='fai:my_model',
            meta={
                'name': 'cool name',
                'description': 'cool desc',
                'avatar_base64': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==',
                'primary_color': '#facade',
                'sample_questions': ['a', 'b', 'c'],
            }
        )

        result = await service.get_available_assistants(as_uid='john')

        assert result[0].id == aid
        assert result[0].model == 'fai:my_model'
        assert result[0].meta['name'] == 'cool name'
        assert result[0].meta['description'] == 'cool desc'
        assert result[0].meta[
                   'avatar_base64'] == 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=='
        assert result[0].meta['primary_color'] == '#facade'
        assert result[0].meta['sample_questions'] == ['a', 'b', 'c']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_available_assistants_public(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        result1 = await service.get_assistant(as_uid='jane', assistant_id=aid)
        available1 = await service.get_available_assistants(as_uid='jane')

        await service.update_assistant(as_uid='john', assistant_id=aid, is_public=True)
        result2 = await service.get_assistant(as_uid='jane', assistant_id=aid)
        available2 = await service.get_available_assistants(as_uid='jane')

        await service.update_assistant(as_uid='john', assistant_id=aid, is_public=False)
        result3 = await service.get_assistant(as_uid='jane', assistant_id=aid)
        available3 = await service.get_available_assistants(as_uid='jane')

        assert result1 is None
        assert len(available1) == 0

        assert result2.id == aid
        assert len(available2) == 1
        assert next((a for a in available2 if a.id == aid), None) is not None

        assert result3 is None
        assert len(available3) == 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_basic(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        success = await service.update_assistant(
            as_uid='john',
            assistant_id=aid,
            meta={
                'name': 'test assistant',
                'description': 'test description'
            }
        )

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert success is True
        assert result.meta['name'] == 'test assistant'
        assert result.meta['description'] == 'test description'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_consecutive(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        success1 = await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': 'test assistant'},
                                                  extra_llm_params={'a': 'a', 'b': 'b'})
        success2 = await service.update_assistant(as_uid='john', assistant_id=aid,
                                                  meta={'sample_questions': ['hello', 'world']})
        success3 = await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': 'my cool assistant'},
                                                  extra_llm_params={'c': 'c'})

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert success1 is True
        assert success2 is True
        assert success3 is True
        assert result.meta['name'] == 'my cool assistant'
        assert result.meta['sample_questions'] == ['hello', 'world']
        assert result.extra_llm_params['c'] == 'c'
        assert 'a' not in result.extra_llm_params
        assert 'b' not in result.extra_llm_params

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_meta_override(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': 'A'})
        await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': 'B'})

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert result.meta['name'] == 'B'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_meta_preserve(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': 'A', 'foo': 'bar'})
        await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': 'B'})

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert result.meta['foo'] == 'bar'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_meta_unset(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': 'A', 'foo': 'baz'})
        await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': None})

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert result.meta['foo'] == 'baz'
        assert 'name' not in result.meta

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_meta_override_array(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        await service.update_assistant(as_uid='john', assistant_id=aid, meta={'name': 'A', 'foo': ['a', 'b', 'c']})
        await service.update_assistant(as_uid='john', assistant_id=aid, meta={'foo': ['d', 'e']})

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert result.meta['foo'] == ['d', 'e']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_full(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        success = await service.update_assistant(
            as_uid='john',
            assistant_id=aid,
            is_public=True,
            model='f',
            llm_api_key='g',
            instructions='h',
            collection_id='i',
            max_collection_results=5,
            extra_llm_params={
                'some_float': 3.1415,
                'some_int': 1337,
                'some_bool': True,
                'some_str': 'j',
                'response_format': {
                    'type': 'json_schema',
                    'json_schema': {
                        'name': 'example_schema',
                        'strict': True,
                        'schema': {
                            'type': 'object',
                            'properties': {'score': {'type': 'number'}},
                            'required': ['score'],
                            'additionalProperties': False
                        },
                    }
                }
            },
            meta={
                'name': 'a',
                'description': 'b',
                'avatar_base64': 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==',
                'primary_color': '#facade',
                'allow_files': True,
                'sample_questions': ['c', 'd', 'e'],
            }
        )

        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert success is True
        assert result.id == aid
        assert result.owner == 'john'
        assert result.model == 'f'
        assert result.instructions == 'h'
        assert result.extra_llm_params['some_float'] == 3.1415
        assert result.extra_llm_params['some_int'] == 1337
        assert result.extra_llm_params['some_bool'] is True
        assert result.extra_llm_params['some_str'] == 'j'
        assert result.extra_llm_params['response_format'] == {
            'type': 'json_schema',
            'json_schema': {
                'name': 'example_schema',
                'strict': True,
                'schema': {
                    'type': 'object',
                    'properties': {'score': {'type': 'number'}},
                    'required': ['score'],
                    'additionalProperties': False
                },
            }
        }
        assert result.collection_id == 'i'
        assert result.max_collection_results == 5
        assert result.meta['is_public'] is True
        assert result.meta['name'] == 'a'
        assert result.meta['description'] == 'b'
        assert result.meta[
                   'avatar_base64'] == 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=='
        assert result.meta['primary_color'] == '#facade'
        assert result.meta['allow_files'] is True
        assert result.meta['sample_questions'] == ['c', 'd', 'e']

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_invalid_uid(service: IAssistantService):
        aid = await service.create_assistant(as_uid='john')

        success = await service.update_assistant(as_uid='jane', assistant_id=aid, meta={'name': 'evil override'})
        result = await service.get_assistant(as_uid='john', assistant_id=aid)

        assert success is False
        assert 'name' not in result.meta

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_invalid_assistant_id(service: IAssistantService):
        success = await service.update_assistant(as_uid='john', assistant_id='invalid', meta={'name': 'hello'})
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
