from tempfile import NamedTemporaryFile
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Security, UploadFile
from more_itertools import chunked

from fai_backend.collection.dependencies import get_collection_service
from fai_backend.collection.service import CollectionService
from fai_backend.config import settings
from fai_backend.dependencies import get_authenticated_user, get_page_template_for_logged_in_users, get_project_user
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.file_parser import ParserFactory, is_url
from fai_backend.files.service import FileUploadService
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.phrase import phrase as _
from fai_backend.schema import ProjectUser
from fai_backend.vector.dependencies import get_vector_service
from fai_backend.vector.service import VectorService

router_base = APIRouter()

router = APIRouter(
    prefix='/api',
    tags=['Documents'],
)


@router.get('/documents', response_model=list, response_model_exclude_none=True)
async def list_view(
        file_service: FileUploadService = Depends(get_file_upload_service),
        collection_service: CollectionService = Depends(get_collection_service),
        project_user: ProjectUser = Depends(get_project_user),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    files = file_service.list_files(project_user.project_id)
    most_recent_collection = max(files, key=lambda file: file.upload_date).collection if files else []
    most_recent_upload_files = [file for file in files if file.collection == most_recent_collection]

    collection_label = await collection_service.get_collection_metadata_label_or_empty_string(most_recent_collection)
    if not collection_label:
        collection_label = most_recent_collection

    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Div(components=[
                    c.Text(text=f'Collection {collection_label}'),
                    c.Div(components=[
                        c.Table(
                            data=[
                                {
                                    'file_name': file.file_name,
                                    'file_size': file.file_size.human_readable(),
                                    'collection': file.collection,
                                    'mime_type': file.mime_type,
                                    'upload_date': file.upload_date.date(),
                                }
                                for file in most_recent_upload_files
                            ],
                            columns=[
                                {'key': 'file_name', 'label': _('file_name', 'File name')},
                                {'key': 'collection', 'label': _('collection', 'Collection')},
                                {'key': 'file_size', 'label': _('file_size', 'File size')},
                                {'key': 'mime_type', 'label': _('mime_type', 'Mime type')},
                                {'key': 'upload_date', 'label': _('upload_date', 'Upload date')},
                            ],

                            class_name='text-base-content join-item md:table-sm lg:table-md table-auto',
                        ),
                    ], class_name='overflow-x-auto space-y-4'),
                ], class_name='card bg-base-100 w-full max-w-6xl'),
            ], class_name='card-body'),
        ], class_name='card')],
        _('documents', 'Documents'),
    )


@router.get('/documents/upload', response_model=list, response_model_exclude_none=True)
def upload_view(view=Depends(get_page_template_for_logged_in_users)) -> list:
    return view(
        [c.Div(components=[
            c.Div(components=[
                c.Form(
                    submit_as='form',
                    submit_url='/api/documents/upload_and_vectorize',
                    components=[
                        c.InputField(
                            name='collection_label',
                            label=_('Collection label (optional)'),
                            placeholder=_('Collection label (optional)'),
                            required=False,
                            html_type='text',
                        ),
                        c.Textarea(
                            name='urls',
                            placeholder=_('urls', 'URLs'),
                            label=_('urls', 'URLs'),
                            required=False,
                            class_name='whitespace-nowrap',
                            rows=6
                        ),
                        c.FileInput(
                            name='files',
                            label=_('file', 'File'),
                            required=False,
                            multiple=True,
                            file_size_limit=settings.FILE_SIZE_LIMIT,
                        ),
                        c.Button(
                            html_type='submit',
                            label=_('upload', 'Upload'),
                            class_name='btn btn-primary',
                        ),
                    ],
                    class_name='card-body',
                ),
            ], class_name='card bg-base-100 w-full max-w-xl'),
        ])], _('upload_documents', 'Upload documents'))


@router.post('/documents/upload_and_vectorize', response_model=list, response_model_exclude_none=True)
async def upload_and_vectorize_handler(
        files: Annotated[
            list[UploadFile], File(description='Multiple files as UploadFile')
        ],
        collection_label: str = Form(None),
        urls: str = Form(None),
        project_user: ProjectUser = Depends(get_project_user),
        file_service: FileUploadService = Depends(get_file_upload_service),
        vector_service: VectorService = Depends(get_vector_service),
        view=Depends(get_page_template_for_logged_in_users),
        collection_service: CollectionService = Depends(get_collection_service),
) -> list:
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

    list_of_files = [file for file in files if len(file.filename) > 0]
    list_of_urls = [url for url in (urls or '').splitlines() if is_url(url)]

    upload_path = file_service.save_files(project_user.project_id, list_of_files)
    collection_name = upload_path.split('/')[-1]

    await vector_service.create_collection(
        collection_name=collection_name,
        embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL
    )

    for batch in chunked(
            generate_chunks([
                *[file.path for file in file_service.get_file_infos(upload_path)],
                *list_of_urls
            ]),
            100
    ):
        await vector_service.add_documents_without_id_to_empty_collection(
            collection_name=collection_name,
            documents=[chunk['document'] for chunk in batch],
            embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL,
            documents_metadata=[chunk['document_meta'] for chunk in batch],
            document_ids=[chunk['document_id'] for chunk in batch]
        )

    await collection_service.create_collection_metadata(
        collection_id=collection_name or '',
        label=collection_label or '',
        description='',
        embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL,
        urls=[url for url in list_of_urls]
    )

    return view(
        c.FireEvent(event=e.GoToEvent(url='/documents')),
        _('submit_a_question', 'Create Question'),
    )


@router.post('/document/parse', dependencies=[Security(get_authenticated_user)])
def parse_document(
        file: UploadFile
):
    with NamedTemporaryFile(delete=False) as temp:
        temp.write(file.file.read())
        temp.flush()
        parser = ParserFactory.get_parser(temp.name)
        parsed = parser.parse(temp.name)
        joined = '\n\n'.join([p.text for p in parsed])
        return joined
