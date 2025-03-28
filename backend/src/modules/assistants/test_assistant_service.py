import pytest

from src.modules.assistants.protocols.IAssistantService import IAssistantService


class BaseAssistantServiceTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_assistant(service: IAssistantService):
        result = await service.create_assistant()

        assert result
        assert len(result) > 0

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistant(service: IAssistantService):
        assistant_id = await service.create_assistant()

        result = await service.get_assistant(assistant_id)

        assert result
        assert result.id == assistant_id

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistant_invalid(service: IAssistantService):
        result = await service.get_assistant('does not exist')

        assert result is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_assistants(service: IAssistantService):
        assistant1 = await service.create_assistant()
        assistant2 = await service.create_assistant()

        result = await service.get_assistants()

        assert len(result) == 2
        assert next(a for a in result if a.id == assistant1)
        assert next(a for a in result if a.id == assistant2)

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant(service: IAssistantService):
        assistant_id = await service.create_assistant()
        result = await service.update_assistant(
            assistant_id,
            name='my assistant',
            description='my description',
            allow_files=True,
            sample_questions=['a', 'b'],
            model='model_name',
            llm_api_key='api_key',
            instructions='instructions here',
            temperature=0.31415,
            max_tokens=16000,
            collection_id='my_collection_id',
        )

        assistant = await service.get_assistant(assistant_id)

        assert result
        assert assistant.meta.name == 'my assistant'
        assert assistant.meta.description == 'my description'
        assert assistant.meta.allow_files is True
        assert assistant.meta.sample_questions == ['a', 'b']
        assert assistant.model == 'model_name'
        assert assistant.llm_api_key == 'api_key'
        assert assistant.instructions == 'instructions here'
        assert assistant.temperature == 0.31415
        assert assistant.max_tokens == 16000
        assert assistant.collection_id == 'my_collection_id'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_assistant_invalid(service: IAssistantService):
        result = await service.update_assistant(
            'does not exist',
            name='my assistant',
            description='my description',
            allow_files=True,
            sample_questions=['a', 'b'],
            model='model_name',
            llm_api_key='api_key',
            instructions='instructions here',
            temperature=0.31415,
            max_tokens=16000,
            collection_id='my_collection_id',
        )
        assert result is False

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_assistant(service: IAssistantService):
        assistant_id = await service.create_assistant()

        await service.delete_assistant(assistant_id)
        assistant = await service.get_assistant(assistant_id)

        assert assistant is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_assistant_invalid(service: IAssistantService):
        await service.delete_assistant('does not exist')
        assistant = await service.get_assistant('does not exist')

        assert assistant is None
