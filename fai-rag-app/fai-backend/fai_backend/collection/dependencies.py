from fai_backend.collection.service import CollectionService
from fai_backend.repositories import collection_metadata_repo


def get_collection_service() -> CollectionService:
    return CollectionService(collection_metadata_repo)
