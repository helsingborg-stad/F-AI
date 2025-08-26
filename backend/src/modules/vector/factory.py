import os

from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.vector.ChromaDBClientVectorService import ChromaDBClientVectorService
from src.modules.vector.ChromaDBLocalVectorService import ChromaDBLocalVectorService
from src.modules.vector.protocols.IVectorService import IVectorService


class VectorServiceFactory:
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    def get(self) -> IVectorService:
        server_host = os.environ.get("CHROMADB_HOST")
        server_port = os.environ.get("CHROMADB_PORT")

        if server_host is not None and len(server_host) > 0:
            port = int(server_port) if server_port is not None and server_port.isdigit() else int(server_port)
            return ChromaDBClientVectorService(settings_service=self._settings_service, host=server_host, port=port)

        return ChromaDBLocalVectorService(settings_service=self._settings_service)
