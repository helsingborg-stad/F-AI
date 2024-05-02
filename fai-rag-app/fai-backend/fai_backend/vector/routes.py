from fastapi import Depends, APIRouter, HTTPException, status

from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.vector.dependencies import get_vector_service
from fai_backend.vector.service import VectorService
from fai_backend.vector.schema import VectorData
from fai_backend.vector.router_error_handler import handle_errors

router = APIRouter(
    prefix='/api',
    tags=['Vector'],
    route_class=LoggingAPIRouter,
)


@router.post('/vector/create_collection', response_model=dict)
@handle_errors
async def create_collection(
        collection_name: str,
        vector_service: VectorService = Depends(get_vector_service)
):
    await vector_service.create_collection(collection_name=collection_name)

    return {
        "message": "Successfully created collection",
        "collection_name": collection_name,
    }


@router.post('/vector/delete_collection', response_model=dict)
@handle_errors
async def delete_collection(
        collection_name: str,
        vector_service: VectorService = Depends(get_vector_service)
):
    await vector_service.delete_collection(collection_name=collection_name)

    return {
        "message": "Successfully deleted collection",
        "collection_name": collection_name,
    }


@router.post('/vector/add_to_collection', response_model=dict)
@handle_errors
async def add_to_collection(
        collection_name: str,
        json: VectorData,
        vector_service: VectorService = Depends(get_vector_service)
):
    artifacts = json.artifacts
    ids = [str(i) for i in range(len(artifacts))]
    documents = [str(elem) for elem in artifacts]

    await vector_service.add_to_collection(
        collection_name=collection_name,
        ids=ids,
        documents=documents,
    )

    return {
        "message": "Successfully added to collection",
        "collection_name": collection_name,
        "added_count": len(artifacts),
    }


@router.get('/vector/query_collection', response_model=dict)
@handle_errors
async def query_vector(
        collection_name: str,
        query_text: str,
        n_results: int = 10,
        vector_service: VectorService = Depends(get_vector_service)
):
    results = await vector_service.query_from_collection(
        collection_name=collection_name,
        query_texts=[query_text],
        n_results=n_results,
    )

    return {
        "message": "Successfully queried collection",
        "collection_name": collection_name,
        "results": results,
    }


@router.get('/vector/list_collections', response_model=dict)
@handle_errors
async def list_collections(
        vector_service: VectorService = Depends(get_vector_service)
):
    collections = await vector_service.list_collections()

    return {
        "message": "Successfully listed collections",
        "collections": list(collections),
    }
