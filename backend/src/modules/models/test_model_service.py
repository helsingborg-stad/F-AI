import pytest

from src.modules.models.models.Model import Model
from src.modules.models.protocols.IModelService import IModelService


class BaseModelServiceTestClass:
    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_available_models(service: IModelService):
        success = await service.set_available_models(models=[
            Model(key='a', provider='A', display_name='Cool Model A', description='cool model A'),
            Model(key='b', provider='B', display_name='Cool Model B', description='cool model B'),
            Model(key='c', provider='C', display_name='Cool Model C', description='cool model C'),
        ])

        models = await service.get_available_models(as_uid='john')
        models_by_key = {model.key: model for model in models}

        assert success
        assert len(models) == 3
        assert models_by_key['a'].provider == 'A'
        assert models_by_key['a'].display_name == 'Cool Model A'
        assert models_by_key['a'].description == 'cool model A'
        assert models_by_key['b'].provider == 'B'
        assert models_by_key['b'].display_name == 'Cool Model B'
        assert models_by_key['b'].description == 'cool model B'
        assert models_by_key['c'].provider == 'C'
        assert models_by_key['c'].display_name == 'Cool Model C'
        assert models_by_key['c'].description == 'cool model C'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_available_models_override(service: IModelService):
        success1 = await service.set_available_models(models=[
            Model(key='a', provider='A', display_name='Cool Model A', description='my cool model A'),
            Model(key='b', provider='B', display_name='Cool Model B', description='my cool model B'),
            Model(key='c', provider='C', display_name='Cool Model C', description='my cool model C'),
        ])

        success2 = await service.set_available_models(models=[
            Model(key='D', provider='d', display_name='cool model D', description='my cool model D'),
        ])

        models = await service.get_available_models(as_uid='john')
        models_by_key = {model.key: model for model in models}

        assert success1
        assert success2
        assert len(models) == 1
        assert models_by_key['D'].provider == 'd'
        assert models_by_key['D'].display_name == 'cool model D'
        assert models_by_key['D'].description == 'my cool model D'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_set_available_models_twice(service: IModelService):
        success1 = await service.set_available_models(models=[])
        success2 = await service.set_available_models(models=[])

        assert success1
        assert success2

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_model(service: IModelService):
        model = Model(
            key='gpt-4',
            provider='openai',
            display_name='GPT-4',
            description='Advanced language model',
            meta={'context_length': 8192},
            status='active',
            visibility='public'
        )
        
        success = await service.create_model(model, as_uid='admin')
        assert success is True
        
        retrieved = await service.get_model('gpt-4', as_uid='admin')
        assert retrieved is not None
        assert retrieved.key == 'gpt-4'
        assert retrieved.provider == 'openai'
        assert retrieved.display_name == 'GPT-4'
        assert retrieved.description == 'Advanced language model'
        assert retrieved.meta == {'context_length': 8192}
        assert retrieved.status == 'active'
        assert retrieved.visibility == 'public'
        assert retrieved.version == 1

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_model_duplicate_key(service: IModelService):
        model1 = Model(
            key='claude-3',
            provider='anthropic',
            display_name='Claude 3',
            description='Anthropic model',
            status='active',
            visibility='public'
        )
        
        model2 = Model(
            key='claude-3',
            provider='anthropic-v2',
            display_name='Claude 3 V2',
            description='Updated Anthropic model',
            status='active',
            visibility='public'
        )
        
        success1 = await service.create_model(model1, as_uid='admin')
        assert success1 is True
        
        success2 = await service.create_model(model2, as_uid='admin')
        assert success2 is False
        
        retrieved = await service.get_model('claude-3', as_uid='admin')
        assert retrieved.provider == 'anthropic'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_model(service: IModelService):
        model = Model(
            key='llama-2',
            provider='meta',
            display_name='Llama 2',
            description='Open source LLM',
            status='active',
            visibility='public'
        )
        
        await service.create_model(model, as_uid='admin')
        
        retrieved = await service.get_model('llama-2', as_uid='admin')
        assert retrieved is not None
        assert retrieved.key == 'llama-2'
        assert retrieved.provider == 'meta'
        assert retrieved.display_name == 'Llama 2'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_model_not_found(service: IModelService):
        retrieved = await service.get_model('non-existent-model', as_uid='admin')
        assert retrieved is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_model(service: IModelService):
        model = Model(
            key='gemini-pro',
            provider='google',
            display_name='Gemini Pro',
            description='Google AI model',
            status='active',
            visibility='public'
        )
        
        await service.create_model(model, as_uid='admin')
        
        updated_model = Model(
            key='gemini-pro',
            provider='google-ai',
            display_name='Gemini Pro Updated',
            description='Enhanced Google AI model',
            meta={'enhanced': True},
            status='deprecated',
            visibility='internal',
            version=1
        )
        
        success = await service.update_model('gemini-pro', updated_model, as_uid='admin')
        assert success is True
        
        retrieved = await service.get_model('gemini-pro', as_uid='admin')
        assert retrieved.provider == 'google-ai'
        assert retrieved.display_name == 'Gemini Pro Updated'
        assert retrieved.description == 'Enhanced Google AI model'
        assert retrieved.meta == {'enhanced': True}
        assert retrieved.status == 'deprecated'
        assert retrieved.visibility == 'internal'
        assert retrieved.version == 2

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_model(service: IModelService):
        model = Model(
            key='mixtral-8x7b',
            provider='mistral',
            display_name='Mixtral 8x7B',
            description='Mixture of experts model',
            status='active',
            visibility='public'
        )
        
        await service.create_model(model, as_uid='admin')
        
        success = await service.delete_model('mixtral-8x7b', as_uid='admin')
        assert success is True
        
        retrieved = await service.get_model('mixtral-8x7b', as_uid='admin')
        assert retrieved is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_create_model_with_slash_in_key(service: IModelService):
        model = Model(
            key='xai/grok-3-mini-beta',
            provider='xai',
            display_name='Grok 3 Mini Beta',
            description='xAI language model',
            status='active',
            visibility='public'
        )
        
        success = await service.create_model(model, as_uid='admin')
        assert success is True
        
        retrieved = await service.get_model('xai/grok-3-mini-beta', as_uid='admin')
        assert retrieved is not None
        assert retrieved.key == 'xai/grok-3-mini-beta'
        assert retrieved.provider == 'xai'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_get_model_with_slash_in_key(service: IModelService):
        model = Model(
            key='anthropic/claude-instant',
            provider='anthropic',
            display_name='Claude Instant',
            description='Fast Anthropic model',
            status='active',
            visibility='public'
        )
        
        await service.create_model(model, as_uid='admin')
        
        retrieved = await service.get_model('anthropic/claude-instant', as_uid='admin')
        assert retrieved is not None
        assert retrieved.key == 'anthropic/claude-instant'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_model_with_slash_in_key(service: IModelService):
        model = Model(
            key='openai/gpt-3.5-turbo',
            provider='openai',
            display_name='GPT-3.5 Turbo',
            description='Fast OpenAI model',
            status='active',
            visibility='public'
        )
        
        await service.create_model(model, as_uid='admin')
        
        updated_model = Model(
            key='openai/gpt-3.5-turbo',
            provider='openai-v2',
            display_name='GPT-3.5 Turbo Updated',
            description='Enhanced fast OpenAI model',
            status='deprecated',
            visibility='internal',
            version=1
        )
        
        success = await service.update_model('openai/gpt-3.5-turbo', updated_model, as_uid='admin')
        assert success is True
        
        retrieved = await service.get_model('openai/gpt-3.5-turbo', as_uid='admin')
        assert retrieved.provider == 'openai-v2'
        assert retrieved.display_name == 'GPT-3.5 Turbo Updated'

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_delete_model_with_slash_in_key(service: IModelService):
        model = Model(
            key='meta/llama-2-70b',
            provider='meta',
            display_name='Llama 2 70B',
            description='Large Llama model',
            status='active',
            visibility='public'
        )
        
        await service.create_model(model, as_uid='admin')
        
        success = await service.delete_model('meta/llama-2-70b', as_uid='admin')
        assert success is True
        
        retrieved = await service.get_model('meta/llama-2-70b', as_uid='admin')
        assert retrieved is None

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_update_model_optimistic_locking(service: IModelService):
        model = Model(
            key='concurrent-model',
            provider='test',
            display_name='Concurrent Model',
            description='Model for testing optimistic locking',
            status='active',
            visibility='public'
        )
        
        await service.create_model(model, as_uid='admin')
        
        update1 = Model(
            key='concurrent-model',
            provider='test-v1',
            display_name='Concurrent Model V1',
            description='First update',
            status='active',
            visibility='public',
            version=1
        )
        
        success1 = await service.update_model('concurrent-model', update1, as_uid='admin')
        assert success1 is True
        
        update2 = Model(
            key='concurrent-model',
            provider='test-v2',
            display_name='Concurrent Model V2',
            description='Second update',
            status='active',
            visibility='public',
            version=1
        )
        
        success2 = await service.update_model('concurrent-model', update2, as_uid='admin')
        assert success2 is False
        
        retrieved = await service.get_model('concurrent-model', as_uid='admin')
        assert retrieved.provider == 'test-v1'
        assert retrieved.version == 2

    @staticmethod
    @pytest.mark.asyncio
    @pytest.mark.mongo
    async def test_model_lifecycle_fields(service: IModelService):
        import asyncio
        model = Model(
            key='lifecycle-model',
            provider='test',
            display_name='Lifecycle Model',
            description='Testing lifecycle fields',
            status='active',
            visibility='public'
        )
        
        await service.create_model(model, as_uid='admin')
        
        retrieved = await service.get_model('lifecycle-model', as_uid='admin')
        assert retrieved.created_at is not None
        assert retrieved.updated_at is not None
        created_at = retrieved.created_at
        
        await asyncio.sleep(0.1)
        
        update = Model(
            key='lifecycle-model',
            provider='test-updated',
            display_name='Lifecycle Model Updated',
            description='Updated description',
            status='active',
            visibility='public',
            version=1
        )
        
        await service.update_model('lifecycle-model', update, as_uid='admin')
        
        retrieved2 = await service.get_model('lifecycle-model', as_uid='admin')
        assert retrieved2.created_at == created_at
        assert retrieved2.updated_at > created_at