from fai_backend.vector.service import VectorService
from fai_backend.vector.factory import vector_db


async def get_vector_service():
    return VectorService(vector_db)
