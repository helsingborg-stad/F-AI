import os
from tempfile import TemporaryDirectory

from fastapi import APIRouter, status, UploadFile
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator

collection_router = APIRouter(
    prefix='/collection',
    tags=['Collection']
)

auth = AuthRouterDecorator(collection_router)


class CreateCollectionRequest(BaseModel):
    label: str
    embedding_model: str


@auth.post(
    '',
    required_scopes=['can_manage_collections'],
    summary='Create a collection',
    description='Create a collection',
)
async def create_collection(body: CreateCollectionRequest, services: ServicesDependency):
    await services.collection_service.create(
        label=body.label,
        embedding_model=body.embedding_model,
    )


class GetCollectionResponseCollection(BaseModel):
    id: str
    label: str
    embedding_model: str
    files: list[str]
    urls: list[str]


class GetCollectionsResponse(BaseModel):
    collections: list[GetCollectionResponseCollection]


@auth.get(
    '',
    required_scopes=['can_manage_collections'],
    summary='Get collections',
    description='Get collections',
)
async def get_collections(services: ServicesDependency):
    collections = await services.collection_service.list_collections()
    return GetCollectionsResponse(collections=[
        GetCollectionResponseCollection(
            id=collection.id,
            label=collection.label,
            embedding_model=collection.embedding_model,
            files=collection.files,
            urls=collection.urls
        ) for collection in collections
    ])


@auth.delete(
    '/{collection_id}',
    required_scopes=['can_manage_collections'],
    summary='Delete a collection',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_collection(collection_id: str, services: ServicesDependency):
    await services.collection_service.delete(collection_id)


class UpdateCollectionRequest(BaseModel):
    label: str


@auth.patch(
    '/{collection_id}',
    required_scopes=['can_manage_collections'],
    summary='Update collection metadata',
)
async def update_collection_metadata(body: UpdateCollectionRequest, collection_id: str, services: ServicesDependency):
    await services.collection_service.set_collection_meta(collection_id, body.label)


@auth.put(
    '/{collection_id}/content',
    required_scopes=['can_manage_collections'],
    summary='Replace content (files/urls) of a collection',
)
async def set_collection_content(
        collection_id: str,
        services: ServicesDependency,
        files: list[UploadFile] = None,
        urls: list[str] = None
):
    # Weird hack (?) for FastAPI handling multipart/form-data string array as a single comma-separated string
    urls = urls[0].split(',') if urls and len(urls) > 0 else []

    with TemporaryDirectory() as temp_dir:
        file_paths = []
        if files and len(files) > 0:
            for file in files:
                temp_file_path = os.path.join(temp_dir, file.filename)
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(file.file.read())
                    file_paths.append(temp_file_path)

        paths_and_urls = [p for p in file_paths + (urls or []) if len(p) > 0]

        await services.collection_service.set_collection_documents(collection_id, paths_and_urls)


class QueryCollectionRequest(BaseModel):
    query: str


class QueryCollectionResponseResult(BaseModel):
    content: str
    source: str
    page_number: int | None


class QueryCollectionResponse(BaseModel):
    results: list[QueryCollectionResponseResult]


@auth.post(
    '/{collection_id}/query',
    required_scopes=['can_manage_collections'],
)
async def query_collection(body: QueryCollectionRequest, collection_id: str, services: ServicesDependency):
    results = await services.collection_service.query(collection_id, body.query, max_results=10)
    return QueryCollectionResponse(
        results=[
            QueryCollectionResponseResult(
                content=result.content,
                source=result.source,
                page_number=result.page_number
            ) for result in results
        ]
    )
