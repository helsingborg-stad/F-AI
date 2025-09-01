import pytest
from pydantic import ValidationError

from src.modules.models.models.Model import Model


class TestModel:
    def test_valid_model_creation(self):
        model = Model(
            key='gpt-4',
            provider='openai',
            display_name='GPT-4',
            description='Advanced language model'
        )
        assert model.key == 'gpt-4'
        assert model.provider == 'openai'
        assert model.display_name == 'GPT-4'
        assert model.description == 'Advanced language model'
        assert model.status == 'active'
        assert model.visibility == 'public'
        assert model.version == 1

    def test_valid_model_with_slash_key(self):
        model = Model(
            key='anthropic/claude-3',
            provider='anthropic',
            display_name='Claude 3'
        )
        assert model.key == 'anthropic/claude-3'

    def test_valid_model_with_dots_and_hyphens(self):
        model = Model(
            key='gpt-3.5-turbo',
            provider='openai',
            display_name='GPT-3.5 Turbo'
        )
        assert model.key == 'gpt-3.5-turbo'

    def test_key_empty_string_fails(self):
        with pytest.raises(ValidationError) as exc_info:
            Model(
                key='',
                provider='test',
                display_name='Test Model'
            )
        assert 'key' in str(exc_info.value)

    def test_key_with_spaces_fails(self):
        with pytest.raises(ValidationError) as exc_info:
            Model(
                key='model name with spaces',
                provider='test',
                display_name='Test Model'
            )
        assert 'key' in str(exc_info.value)

    def test_key_with_invalid_characters_fails(self):
        invalid_keys = [
            'model@name',
            'model#name',
            'model name',
            'model+name',
            'model!name',
            'model(name)',
            'model[name]',
            'model{name}',
        ]
        
        for invalid_key in invalid_keys:
            with pytest.raises(ValidationError) as exc_info:
                Model(
                    key=invalid_key,
                    provider='test',
                    display_name='Test Model'
                )
            assert 'key' in str(exc_info.value)

    def test_provider_empty_string_fails(self):
        with pytest.raises(ValidationError) as exc_info:
            Model(
                key='test-model',
                provider='',
                display_name='Test Model'
            )
        assert 'provider' in str(exc_info.value)

    def test_display_name_empty_string_fails(self):
        with pytest.raises(ValidationError) as exc_info:
            Model(
                key='test-model',
                provider='test',
                display_name=''
            )
        assert 'display_name' in str(exc_info.value)

    def test_display_name_too_long_fails(self):
        long_name = 'A' * 101
        
        with pytest.raises(ValidationError) as exc_info:
            Model(
                key='test-model',
                provider='test',
                display_name=long_name
            )
        assert 'display_name' in str(exc_info.value)

    def test_display_name_exactly_100_chars_passes(self):
        name_100_chars = 'A' * 100
        
        model = Model(
            key='test-model',
            provider='test',
            display_name=name_100_chars
        )
        assert len(model.display_name) == 100

    def test_display_name_single_character_passes(self):
        model = Model(
            key='test-model',
            provider='test',
            display_name='A'
        )
        assert model.display_name == 'A'