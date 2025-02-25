import os.path
from tempfile import TemporaryDirectory

from fastapi import APIRouter, UploadFile, HTTPException
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.common.is_url import is_url

document_chunker_router = APIRouter(
    prefix='/document/chunk',
    tags=['Document Chunking'],
)

auth = AuthRouterDecorator(document_chunker_router)


class ChunkDocumentResponseChunk(BaseModel):
    content: str
    source: str
    pageNumber: int | None


class ChunkDocumentResponse(BaseModel):
    chunks: list[ChunkDocumentResponseChunk]


@auth.post(
    '/file',
    required_scopes=['can_manage_documents'],
    summary='Chunk a file',
    description='''
Parse and split a file into string parts (chunks) based on file-type specific semantics.

Supported file types: PDF, Word, Excel, HTML, Markdown, plain text.
    ''',
    response_description='''
Chunks of the file with associated metadata.
    ''',
    response_model=ChunkDocumentResponse,
    response_400_description='Invalid (unsupported) file type.'
)
async def chunk_file(file: UploadFile, services: ServicesDependency):
    with TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, file.filename)
        print(f'temp_file_path: {temp_file_path}')
        with open(temp_file_path, 'wb') as new_file:
            new_file.write(file.file.read())

        try:
            chunker = services.document_chunker_factory.get(temp_file_path)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        chunks = chunker.chunk(temp_file_path)
        return ChunkDocumentResponse(chunks=[
            ChunkDocumentResponseChunk(
                content=chunk.content,
                source=chunk.source,
                pageNumber=chunk.page_number
            ) for chunk in chunks
        ])


@auth.post(
    '/url',
    required_scopes=['can_manage_documents'],
    summary='Chunk a file/document from an URL',
    description='''
Chunk a file/web-page from an URL.

File/web-page type is determined by a HEAD request to the given URL and using the `Content-Type` response header.

Supported file types: PDF, Word, Excel, HTML, Markdown, plain text.
    ''',
    response_description='''
Chunks of the file/web-page with associated metadata.
    ''',
    response_model=ChunkDocumentResponse,
    response_400_description='Invalid URL.'
)
async def chunk_url(url: str, services: ServicesDependency):
    if not is_url(url):
        raise HTTPException(status_code=400, detail='Only http/https supported')

    chunker = services.document_chunker_factory.get(url)
    chunks = chunker.chunk(url)
    return ChunkDocumentResponse(chunks=[
        ChunkDocumentResponseChunk(
            content=chunk.content,
            source=chunk.source,
            pageNumber=chunk.page_number
        ) for chunk in chunks
    ])
