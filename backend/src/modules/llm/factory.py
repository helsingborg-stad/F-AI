from src.modules.llm.AnthropicLLMService import AnthropicLLMService
from src.modules.llm.OpenAILLMService import OpenAILLMService
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.llm.protocols import ILLMService


class LLMServiceFactory:
    def get(self, model_key: str) -> ILLMService:
        [model_provider, _] = parse_model_key(model_key)

        match model_provider:
            case 'openai':
                return OpenAILLMService()
            case 'anthropic':
                return AnthropicLLMService()
            case _:
                raise ValueError(f'Invalid model key: {model_key}')
