from src.modules.vector.ChromaDBVectorService import ChromaDBVectorService
from src.modules.vector.protocols.IVectorService import IVectorService


class VectorServiceFactory:
    def get(self) -> IVectorService:
        return ChromaDBVectorService()
