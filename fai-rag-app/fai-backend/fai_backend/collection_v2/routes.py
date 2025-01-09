from typing import Union

from fastapi import APIRouter, HTTPException, UploadFile, Depends
from pydantic import BaseModel

from fai_backend.collection_v2.dependencies import get_collection_service
from fai_backend.dependencies import get_project_user
from fai_backend.schema import ProjectUser

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
async def create_collection(data: CreateCollectionRequest, _: ProjectUser = Depends(get_project_user)):
    service = await get_collection_service()
    new_collection = await service.create_collection(
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
async def list_collections(_: ProjectUser = Depends(get_project_user)):
    service = await get_collection_service()
    all_collections = await service.get_collections()
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
async def get_collection(id: str, _: ProjectUser = Depends(get_project_user)):
    service = await get_collection_service()
    collection = await service.get_collection(id)

    if collection is None:
        raise HTTPException(status_code=404, detail='Collection not found')

    return GetCollectionResponse(
        id=collection.collection_id,
        label=collection.label,
        description=collection.description,
        embedding_model=collection.embedding_model,
        urls=collection.urls or []
    )


class UpdateCollectionRequest(BaseModel):
    label: Union[str, None] = None
    description: Union[str, None] = None
    embedding_model: Union[str, None] = None


class UpdateCollectionResponse(BaseModel):
    id: str
    label: str
    description: str
    embedding_model: str
    urls: list[str]


@router.patch(
    '/collections/{id}',
    summary='Update a collection',
    response_model=UpdateCollectionResponse,
)
async def update_collection(id: str, data: UpdateCollectionRequest, _: ProjectUser = Depends(get_project_user)):
    service = await get_collection_service()
    result = await service.update_collection(id, data.dict(exclude_none=True))

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
async def delete_collection(id: str, _: ProjectUser = Depends(get_project_user)):
    service = await get_collection_service()
    await service.delete_collection(id)


@router.put('/collections/{id}/files', summary='Replace collection files')
async def set_collection_files(
        id: str,
        files: list[UploadFile] = None,
        urls: list[str] = None,
        project_user: ProjectUser = Depends(get_project_user)
):
    service = await get_collection_service()
    try:
        await service.set_collection_files(
            collection_id=id,
            project_id=project_user.project_id,
            files=files,
            urls=urls
        )
    except LookupError:
        raise HTTPException(status_code=404, detail='Collection not found')
