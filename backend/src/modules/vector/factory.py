from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.vector.ChromaDBVectorService import ChromaDBVectorService
from src.modules.vector.protocols.IVectorService import IVectorService


class VectorServiceFactory:
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    def get(self) -> IVectorService:
        return ChromaDBVectorService(settings_service=self._settings_service)
