from src.modules.llm.protocols import ILLMService
from src.modules.llm.OpenAILLMService import OpenAILLMService
from src.modules.settings.protocols.ISettingsService import ISettingsService


class LLMServiceFactory:
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    def get(self) -> ILLMService:
        return OpenAILLMService(settings_service=self._settings_service)
