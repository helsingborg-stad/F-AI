from fastapi import Depends

from fai_backend.collection.dependencies import get_collection_service
from fai_backend.collection.service import CollectionService
from fai_backend.vector.factory import vector_db
from fai_backend.vector.service import VectorService


async def get_vector_service(collection_service: CollectionService = Depends(get_collection_service)) -> VectorService:
    return VectorService(vector_db, collection_service)
