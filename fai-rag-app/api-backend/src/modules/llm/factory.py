from .protocols import ILLMService
from .service import LLMService


class LLMFactory:
    async def get(self) -> ILLMService:
        return LLMService()
