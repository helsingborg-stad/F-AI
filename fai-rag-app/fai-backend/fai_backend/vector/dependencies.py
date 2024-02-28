from fai_backend.vector.service import VectorService
from fai_backend.vector.factory import vector_db


async def get_vector_service(
        collection_name: str,
) -> VectorService:
    return VectorService(vector_db=vector_db, collection_name=collection_name)
