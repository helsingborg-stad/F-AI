from typing import Any

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
            urls: list[str] | None = None

    ):
        collection_metadata = CollectionMetadataModel(
            collection_id=collection_id,
            label=label,
            description=description,
            embedding_model=embedding_model,
            urls=urls
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

    async def update_collection_metadata(self, collection_id: str, collection_metadata_patch: dict[str, Any]):
        existing = await self.get_collection_metadata(collection_id)
        if len(existing) <= 0:
            return None

        return await self.repo.update(str(existing[0].id), collection_metadata_patch)

    async def list_collection_ids(self) -> list[str]:
        collections = await self.repo.list()
        collections.reverse()
        return [c.collection_id for c in collections]

    async def list_collections(self) -> list[CollectionMetadataModel]:
        return await self.repo.list()

    async def delete_collection(self, collection_id: str):
        existing = await self.get_collection_metadata(collection_id)
        if len(existing) <= 0:
            return

        return await self.repo.delete(str(existing[0].id))
