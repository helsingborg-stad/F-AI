import uuid
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

from fastapi import UploadFile
from more_itertools import chunked

from fai_backend.collection.models import CollectionMetadataModel, CollectionFile
from fai_backend.files.file_parser import ParserFactory
from fai_backend.files.service import FileUploadService
from fai_backend.repositories import CollectionMetadataRepository
from fai_backend.repository.query.component import AttributeAssignment
from fai_backend.vector.service import VectorService


class CollectionService:
    def __init__(
            self,
            repo: CollectionMetadataRepository,
            vector_service: VectorService,
            file_upload_service: FileUploadService
    ):
        self.repo = repo
        self.vector_service = vector_service
        self.file_upload_service = file_upload_service

    async def create_collection(self, label: str, description: str, embedding_model: str) -> CollectionMetadataModel:
        new_id = str(uuid.uuid4())

        await self.vector_service.create_collection(
            collection_name=new_id,
            embedding_model=embedding_model,
        )

        new_collection = await self._create_collection_metadata(
            collection_id=new_id,
            label=label,
            description=description,
            embedding_model=embedding_model
        )

        return new_collection

    async def get_collections(self) -> list[CollectionMetadataModel]:
        return await self.repo.list()

    async def get_collection(self, collection_id: str) -> CollectionMetadataModel | None:
        query = AttributeAssignment('collection_id', collection_id)

        result = await self.repo.list(query)

        return result[0] if len(result) > 0 else None

    async def update_collection(self, collection_id: str,
                                collection_metadata_patch: dict[str, Any]) -> CollectionMetadataModel | None:
        existing = await self.get_collection(collection_id)
        if existing is None:
            return None

        return await self.repo.update(str(existing.id), collection_metadata_patch)

    async def set_collection_files(
            self,
            collection_id: str,
            project_id: str,
            files: list[UploadFile] = None,
            urls: list[str] = None,
    ):
        files = files or []
        urls = urls or []

        collection = await self.get_collection(collection_id)

        if collection is None:
            raise LookupError('Collection not found')

        try:
            await self.vector_service.delete_collection(collection_id)
        except ValueError:
            pass

        await self.vector_service.create_collection(
            collection_name=collection_id,
            embedding_model=collection.embedding_model
        )

        upload_path = self.file_upload_service.save_files(project_id, files)
        list_of_urls = [url for url in urls if CollectionService._is_url(url)]
        for batch in chunked(
                CollectionService._generate_chunks([
                    *[file.path for file in self.file_upload_service.get_file_infos(upload_path)],
                    *list_of_urls
                ]),
                100
        ):
            await self.vector_service.add_documents_without_id_to_empty_collection(
                collection_name=collection_id,
                documents=[chunk['document'] for chunk in batch],
                embedding_model=collection.embedding_model,
                documents_metadata=[chunk['document_meta'] for chunk in batch],
                document_ids=[chunk['document_id'] for chunk in batch]
            )

        now_timestamp = datetime.utcnow().isoformat()
        collection_files = [
            CollectionFile(
                id=str(uuid.uuid4()),
                name=file.filename,
                upload_timestamp=now_timestamp,
                byte_size=file.size or 0
            )
            for file in files
        ]

        await self.update_collection(collection_id, {'files': collection_files, 'urls': list_of_urls})

    async def delete_collection(self, collection_id: str):
        existing = await self.get_collection(collection_id)
        if existing is None:
            return

        await self.repo.delete(str(existing.id))

    async def _create_collection_metadata(
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

    @staticmethod
    def _is_url(string: str) -> bool:
        parsed = urlparse(string)
        return parsed.scheme in {'http', 'https'}

    @staticmethod
    def _generate_chunks(file_paths_or_urls: list[str]):
        for file_or_url in file_paths_or_urls:
            for element in ParserFactory.get_parser(file_or_url).parse(file_or_url):
                if len(element.text):
                    yield {
                        'document': element.text,
                        'document_meta': {
                            key: value
                            for key, value in element.metadata.to_dict().items()
                            if key in ['filename', 'url', 'page_number', 'page_name']
                        },
                        'document_id': element.id
                    }
