from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, Form, Security, UploadFile

from fai_backend.collection.dependencies import get_collection_service
from fai_backend.collection.service import CollectionService
from fai_backend.config import settings
from fai_backend.dependencies import get_authenticated_user, get_page_template_for_logged_in_users, get_project_user
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.file_parser import ParserFactory, is_url
from fai_backend.files.service import FileUploadService
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.schema import ProjectUser
from fai_backend.vector.dependencies import get_vector_service
from fai_backend.vector.service import VectorService

router = APIRouter(
    prefix='/api',
    tags=['Documents'],
    route_class=LoggingAPIRouter,
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
                        c.FileInput(
                            name='files[]',
                            label=_('file', 'File'),
                            required=False,
                            multiple=True,
                            file_size_limit=settings.FILE_SIZE_LIMIT,
                        ),
                        c.Textarea(
                            name='urls',
                            placeholder=_('urls', 'URLs'),
                            label=_('urls', 'URLs'),
                            required=False,
                            class_name='whitespace-nowrap',
                            rows=6
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
        files: list[UploadFile] = Form([]),
        collection_label: str = Form(None),
        urls: str = Form(None),
        project_user: ProjectUser = Depends(get_project_user),
        file_service: FileUploadService = Depends(get_file_upload_service),
        vector_service: VectorService = Depends(get_vector_service),
        view=Depends(get_page_template_for_logged_in_users),
        collection_service: CollectionService = Depends(get_collection_service),
) -> list:
    upload_path = file_service.save_files(project_user.project_id, files)
    collection_name = upload_path.split('/')[-1]
    chunks = [
        {
            'document': element.text,
            'document_meta': {
                key: value
                for key, value in {**element.metadata.to_dict(), }.items()
                if key in ['filename', 'url', 'page_number', 'page_name']
            }
        }
        for file_or_url in [
            *[file.path for file in file_service.get_file_infos(upload_path)],
            *[url for url in urls.splitlines() if is_url(url)]
        ]
        for element in ParserFactory.get_parser(file_or_url).parse(file_or_url)
    ]

    await vector_service.create_collection(
        collection_name=collection_name,
        embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL
    )

    await vector_service.add_documents_without_id_to_empty_collection(
        collection_name=collection_name,
        documents=[chunk['document'] for chunk in chunks],
        embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL,
        documents_metadata=[chunk['document_meta'] for chunk in chunks],
    )

    await collection_service.create_collection_metadata(
        collection_id=collection_name or '',
        label=collection_label or '',
        description='',
        embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL,
        urls=[url for url in urls.splitlines() if is_url(url)]
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
