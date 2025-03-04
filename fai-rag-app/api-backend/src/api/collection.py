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
)
async def create_collection(body: CreateCollectionRequest, services: ServicesDependency):
    await services.collection_service.create(
        label=body.label,
        embedding_model=body.embedding_model,
    )


class GetCollectionResponseCollectionFile(BaseModel):
    name: str


class GetCollectionResponseCollection(BaseModel):
    id: str
    label: str
    embedding_model: str
    files: list[GetCollectionResponseCollectionFile]
    urls: list[str]


class GetCollectionsResponse(BaseModel):
    collections: list[GetCollectionResponseCollection]


@auth.get(
    '',
    required_scopes=['can_manage_collections'],
    response_model=GetCollectionsResponse
)
async def get_collections(services: ServicesDependency):
    collections = await services.collection_service.list_collections()
    return GetCollectionsResponse(collections=[
        GetCollectionResponseCollection(
            id=collection.id,
            label=collection.label,
            embedding_model=collection.embedding_model,
            files=[GetCollectionResponseCollectionFile(
                name=file.name,
            ) for file in collection.files],
            urls=collection.urls
        ) for collection in collections
    ])


@auth.delete(
    '/{collection_id}',
    required_scopes=['can_manage_collections'],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_collection(collection_id: str, services: ServicesDependency):
    await services.collection_service.delete(collection_id)


class UpdateCollectionRequest(BaseModel):
    label: str


@auth.patch(
    '/{collection_id}',
    required_scopes=['can_manage_collections'],
)
async def update_collection_metadata(body: UpdateCollectionRequest, collection_id: str, services: ServicesDependency):
    await services.collection_service.set_meta(collection_id, body.label)


@auth.put(
    '/{collection_id}/content',
    required_scopes=['can_manage_collections'],
    summary='Replace content (files/urls) of a collection',
    description='''
Replaces the content of the collection with the files/URLs provided.

Note: depending on the size and complexity of the content this may take several minutes
to complete.
    '''
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

        await services.collection_service.set_documents(collection_id, paths_and_urls)


class QueryCollectionRequest(BaseModel):
    query: str
    max_results: int = 10


class QueryCollectionResponseResult(BaseModel):
    content: str
    source: str
    page_number: int | None


class QueryCollectionResponse(BaseModel):
    results: list[QueryCollectionResponseResult]


@auth.post(
    '/{collection_id}/query',
    required_scopes=['can_manage_collections'],
    summary='Query a collection',
    description='''
Query (search) a collection by an input query and returns up to `max_results` (defaults to 10)
chunks of content based on the document(s) in the given collection.

Returned chunks are ordered from most relevant to least relevant content relative to the query.
    ''',
    response_model=QueryCollectionResponse
)
async def query_collection(body: QueryCollectionRequest, collection_id: str, services: ServicesDependency):
    results = await services.collection_service.query(collection_id, body.query, max_results=body.max_results)
    return QueryCollectionResponse(
        results=[
            QueryCollectionResponseResult(
                content=result.content,
                source=result.source,
                page_number=result.page_number
            ) for result in results
        ]
    )
