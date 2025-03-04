from src.modules.llm.protocols import ILLMService
from src.modules.llm.service import LLMService


class LLMServiceFactory:
    def get(self) -> ILLMService:
        return LLMService()
