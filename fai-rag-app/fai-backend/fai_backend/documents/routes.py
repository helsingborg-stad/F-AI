from fastapi import APIRouter, Depends, Form, UploadFile

from fai_backend.collection.dependencies import get_collection_service
from fai_backend.collection.service import CollectionService
from fai_backend.config import settings
from fai_backend.dependencies import get_page_template_for_logged_in_users, get_project_user
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.service import FileUploadService
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import get_project_service, list_projects_request
from fai_backend.projects.schema import ProjectResponse
from fai_backend.projects.service import ProjectService
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
                            title=_('input_fileupload_collection_label',
                                    'Collection label (optional)'),
                            placeholder=_('input_fileupload_collection_placeholder',
                                          'Collection label (optional)'),
                            required=False,
                            html_type='text',
                        ),
                        c.FileInput(
                            name='files',
                            title=_('file', 'File'),
                            required=True,
                            multiple=True,
                            file_size_limit=settings.FILE_SIZE_LIMIT,
                        ),
                        c.Button(
                            html_type='submit',
                            label=_('upload', 'Upload'),
                            class_name='btn btn-primary',
                        ),
                    ],
                    class_name='card bg-base-100 w-full max-w-6xl',
                ),
            ]),
        ])], _('upload_documents', 'Upload documents'))


@router.post('/documents/upload_and_vectorize', response_model=list, response_model_exclude_none=True)
async def upload_and_vectorize_handler(
        files: list[UploadFile],
        collection_label: str = Form(None),
        project_user: ProjectUser = Depends(get_project_user),
        file_service: FileUploadService = Depends(get_file_upload_service),
        vector_service: VectorService = Depends(get_vector_service),
        view=Depends(get_page_template_for_logged_in_users),
        projects: list[ProjectResponse] = Depends(list_projects_request),
        project_service: ProjectService = Depends(get_project_service),
        collection_service: CollectionService = Depends(get_collection_service),
) -> list:
    upload_path = file_service.save_files(project_user.project_id, files)

    upload_directory_name = upload_path.split('/')[-1]
    await vector_service.create_collection(collection_name=upload_directory_name,
                                           embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL)

    parsed_files = file_service.parse_files(upload_path)
    await vector_service.add_documents_without_id_to_empty_collection(
        collection_name=upload_directory_name,
        documents=parsed_files,
        embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL
    )

    await collection_service.create_collection_metadata(
        collection_id=upload_directory_name or '',
        label=collection_label or '',
        description='',
        embedding_model=settings.APP_VECTOR_DB_EMBEDDING_MODEL,
    )

    return view(
        c.FireEvent(event=e.GoToEvent(url='/documents')),
        _('submit_a_question', 'Create Question'),
    )


@router.post('/documents/parse_and_save', response_model=list, response_model_exclude_none=True)
def parse_documents(
        src_directory_path: str,
        dest_directory_path: str,
        dest_file_name: str,
        file_service: FileUploadService = Depends(get_file_upload_service),
) -> list:
    parsed_files = file_service.parse_files(src_directory_path)
    stringify_parsed_files = [str(elem) for elem in parsed_files]

    file_service.dump_list_to_json(stringify_parsed_files, dest_directory_path, dest_file_name)

    return []
