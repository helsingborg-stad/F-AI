from fai_backend.collection_v2.service import CollectionService
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.repositories import collection_metadata_repo
from fai_backend.vector.dependencies import get_vector_service


async def get_collection_service() -> CollectionService:
    return CollectionService(
        repo=collection_metadata_repo,
        vector_service=await get_vector_service(),
        file_upload_service=get_file_upload_service()
    )
