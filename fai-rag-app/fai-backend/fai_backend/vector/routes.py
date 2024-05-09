from pathlib import Path, PurePosixPath

from fastapi import Depends, APIRouter

from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.service import FileUploadService
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
    artifacts = [str(elem) for elem in json.artifacts]
    await vector_service.add_artifacts_to_collection(
        collection_name=collection_name,
        artifacts=artifacts,
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


@router.post('/vector/vectorize_files', response_model=dict)
@handle_errors
async def vectorize_files(
        directory_path: str,
        vector_service: VectorService = Depends(get_vector_service),
        file_service: FileUploadService = Depends(get_file_upload_service),
):
    directory_name = directory_path.split('/')[-1]
    await vector_service.create_collection(collection_name=directory_name)

    parsed_files = file_service.parse_files(directory_path)
    await vector_service.add_artifacts_to_collection(
        collection_name=directory_name,
        artifacts=parsed_files,
    )
