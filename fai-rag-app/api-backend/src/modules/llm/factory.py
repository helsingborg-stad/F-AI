from src.modules.llm.protocols import ILLMService
from src.modules.llm.service import LLMService


class LLMServiceFactory:
    async def get(self) -> ILLMService:
        return LLMService()
