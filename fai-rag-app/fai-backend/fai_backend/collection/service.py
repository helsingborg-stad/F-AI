from fai_backend.collection.models import CollectionMetadataModel
from fai_backend.repositories import CollectionMetadataRepository, collection_metadata_repo


class CollectionService:
    repo: CollectionMetadataRepository

    def __init__(self, repo: collection_metadata_repo):
        self.repo = repo

    async def create_collection_metadata(
            self,
            collection_id: str,
            label: str,
            description: str = '',
    ):
        collection_metadata = CollectionMetadataModel(
            collection_id=collection_id,
            label=label,
            description=description,
        )
        return await self.repo.create(collection_metadata)
