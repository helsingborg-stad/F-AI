from src.modules.llm.AnthropicLLMService import AnthropicLLMService
from src.modules.llm.MistralLLMService import MistralLLMService
from src.modules.llm.OpenAILLMService import OpenAILLMService
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.llm.protocols import ILLMService
from src.modules.settings.protocols.ISettingsService import ISettingsService


class LLMServiceFactory:
    def __init__(self, setting_service: ISettingsService):
        self._setting_service = setting_service

    def get(self, model_key: str) -> ILLMService:
        model_provider, _ = parse_model_key(model_key)

        match model_provider:
            case 'openai':
                return OpenAILLMService(settings_service=self._setting_service)
            case 'anthropic':
                return AnthropicLLMService(settings_service=self._setting_service)
            case 'mistral':
                return MistralLLMService(settings_service=self._setting_service)
            case _:
                raise ValueError(f'Invalid model key: {model_key}')
