from src.modules.llm.OpenAILLMService import OpenAILLMService
from src.modules.llm.protocols import ILLMService


class LLMServiceFactory:
    def get(self) -> ILLMService:
        return OpenAILLMService()
