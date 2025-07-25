from src.modules.ai.completions.LiteLLMCompletionsService import LiteLLMCompletionsService
from src.modules.ai.completions.protocols import ICompletionsService
from src.modules.ai.completions.tools.CompletionsToolsFactory import CompletionsToolsFactory
from src.modules.settings.protocols.ISettingsService import ISettingsService


class CompletionsServiceFactory:
    def __init__(self, setting_service: ISettingsService):
        self._setting_service = setting_service
        self._completions_tools_factory = completions_tools_factory

    def get(self, model: str, api_key: str) -> ICompletionsService:
        return LiteLLMCompletionsService(
            settings_service=self._setting_service,
            model=model,
            api_key=api_key
        )
