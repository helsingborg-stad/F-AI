from fai_backend.collection.models import CollectionMetadataModel
from fai_backend.repositories import CollectionMetadataRepository, collection_metadata_repo
from fai_backend.repository.query.component import AttributeAssignment


class CollectionService:
    repo: CollectionMetadataRepository

    def __init__(self, repo: collection_metadata_repo):
        self.repo = repo

    async def create_collection_metadata(
            self,
            collection_id: str,
            label: str,
            description: str = '',
            embedding_model: str | None = None,

    ):
        collection_metadata = CollectionMetadataModel(
            collection_id=collection_id,
            label=label,
            description=description,
            embedding_model=embedding_model,
        )

        return await self.repo.create(collection_metadata)

    async def get_collection_metadata(self, collection_id: str) -> list[CollectionMetadataModel]:
        query = AttributeAssignment('collection_id', collection_id)

        return await self.repo.list(query)

    async def get_collection_metadata_label_or_empty_string(self, collection_id: str):
        collection_metadata = await self.get_collection_metadata(collection_id)

        label = ''
        if collection_metadata and collection_metadata[0].label:
            label = collection_metadata[0].label

        return label
