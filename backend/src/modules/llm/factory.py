from src.modules.llm.LiteLLMService import LiteLLMService
from src.modules.llm.protocols import ILLMService
from src.modules.settings.protocols.ISettingsService import ISettingsService


class LLMServiceFactory:
    def __init__(self, setting_service: ISettingsService):
        self._setting_service = setting_service

    def get(self) -> ILLMService:
        return LiteLLMService(settings_service=self._setting_service)
