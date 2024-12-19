import uuid
from datetime import datetime
from typing import Union

from fastapi import APIRouter, HTTPException, UploadFile, Depends
from more_itertools import chunked
from pydantic import BaseModel

from fai_backend.collection.dependencies import get_collection_service
from fai_backend.collection.models import CollectionFile
from fai_backend.dependencies import get_project_user
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.file_parser import ParserFactory
from fai_backend.schema import ProjectUser
from fai_backend.vector.dependencies import get_vector_service

router = APIRouter(
    prefix='/api',
    tags=['Collections'],
)


class CreateCollectionRequest(BaseModel):
    label: str
    description: str
    embedding_model: str


class CreateCollectionResponse(BaseModel):
    id: str
    label: str
    description: str
    embedding_model: str


@router.post(
    '/collections',
    summary='Create a new collection',
    status_code=201,
    response_model=CreateCollectionResponse
)
async def create_collection(data: CreateCollectionRequest):
    new_id = str(uuid.uuid4())

    vector_service = await get_vector_service()
    await vector_service.create_collection(
        collection_name=new_id,
        embedding_model=data.embedding_model,
    )

    collection_service = get_collection_service()
    new_collection = await collection_service.create_collection_metadata(
        collection_id=new_id,
        label=data.label,
        description=data.description,
        embedding_model=data.embedding_model
    )
    return CreateCollectionResponse(
        id=new_collection.collection_id,
        label=new_collection.label,
        description=new_collection.description,
        embedding_model=new_collection.embedding_model
    )


class ListCollectionsEntry(BaseModel):
    id: str
    label: str
    description: str


class ListCollectionsResponse(BaseModel):
    data: list[ListCollectionsEntry]


@router.get(
    '/collections',
    summary='Get all collections',
    response_model=ListCollectionsResponse
)
async def list_collections():
    service = get_collection_service()
    all_collections = await service.list_collections()
    return ListCollectionsResponse(
        data=[ListCollectionsEntry(
            id=collection.collection_id,
            label=collection.label,
            description=collection.description
        ) for
            collection in all_collections]
    )


class GetCollectionResponse(BaseModel):
    id: str
    label: str
    description: str
    embedding_model: str
    urls: list[str]


@router.get('/collections/{id}', summary='Get a single collection')
async def get_collection(id: str):
    service = get_collection_service()
    collections = await service.get_collection_metadata(id)

    if len(collections) == 0:
        raise HTTPException(status_code=404, detail='Collection not found')

    return GetCollectionResponse(
        id=collections[0].collection_id,
        label=collections[0].label,
        description=collections[0].description,
        embedding_model=collections[0].embedding_model,
        urls=collections[0].urls or []
    )


class UpdateCollectionRequest(BaseModel):
    label: Union[str, None] = None
    description: Union[str, None] = None
    embedding_model: Union[str, None] = None
    urls: Union[list[str], None] = None


class UpdateCollectionResponse(BaseModel):
    id: str
    label: str
    description: str
    embedding_model: str


@router.patch(
    '/collections/{id}',
    summary='Update a collection',
    response_model=UpdateCollectionResponse,
)
async def update_collection(id: str, data: UpdateCollectionRequest):
    service = get_collection_service()
    result = await service.update_collection_metadata(id, data.dict(exclude_none=True))

    if result is None:
        raise HTTPException(status_code=404, detail='Collection not found')

    return UpdateCollectionResponse(
        id=result.collection_id,
        label=result.label,
        description=result.description,
        embedding_model=result.embedding_model,
        urls=result.urls or []
    )


@router.delete(
    '/collections/{id}',
    summary='Delete a collection',
    status_code=204,
)
async def delete_collection(id: str):
    service = get_collection_service()
    await service.delete_collection(id)


def generate_chunks(file_paths_or_urls: list[str]):
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


@router.put('/collections/{id}/files', summary='Replace collection files')
async def set_collection_files(
        id: str,
        files: list[UploadFile],
        project_user: ProjectUser = Depends(get_project_user)
):
    collection_service = get_collection_service()
    vector_service = await get_vector_service()

    collection = next((c for c in await collection_service.get_collection_metadata(id)), None)

    if collection is None:
        raise HTTPException(status_code=404, detail='Collection not found')

    try:
        await vector_service.delete_collection(id)
    except ValueError:
        pass

    await vector_service.create_collection(
        collection_name=id,
        embedding_model=collection.embedding_model
    )

    file_service = get_file_upload_service()
    upload_path = file_service.save_files(project_user.project_id, files)
    for batch in chunked(
            generate_chunks([
                *[file.path for file in file_service.get_file_infos(upload_path)]
            ]),
            100
    ):
        await vector_service.add_documents_without_id_to_empty_collection(
            collection_name=id,
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

    await collection_service.update_collection_metadata(id, {'files': collection_files})
