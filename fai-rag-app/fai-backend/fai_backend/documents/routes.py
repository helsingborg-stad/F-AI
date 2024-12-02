from tempfile import NamedTemporaryFile

from fastapi import APIRouter, Depends, Form, Security, UploadFile

from fai_backend.collection.dependencies import get_collection_service
from fai_backend.collection.service import CollectionService
from fai_backend.config import settings
from fai_backend.dependencies import get_authenticated_user, get_page_template_for_logged_in_users, get_project_user
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.file_parser import ParserFactory
from fai_backend.files.service import FileUploadService
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import get_project_service, list_projects_request
from fai_backend.projects.schema import ProjectResponse
from fai_backend.projects.service import ProjectService
from fai_backend.schema import ProjectUser
from fai_backend.settings.service import SettingsServiceFactory, SettingKey
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
async def upload_view(view=Depends(get_page_template_for_logged_in_users)) -> list:
    settings_service = SettingsServiceFactory().get_service()
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
                            file_size_limit=await settings_service.get_value(SettingKey.FILE_SIZE_LIMIT),
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

    settings_service = SettingsServiceFactory().get_service()
    embedding_model = await settings_service.get_value(SettingKey.APP_VECTOR_DB_EMBEDDING_MODEL)

    await vector_service.create_collection(collection_name=upload_directory_name,
                                           embedding_model=embedding_model)

    parsed_files = file_service.parse_files(upload_path)
    await vector_service.add_documents_without_id_to_empty_collection(
        collection_name=upload_directory_name,
        documents=parsed_files,
        embedding_model=embedding_model
    )

    await collection_service.create_collection_metadata(
        collection_id=upload_directory_name or '',
        label=collection_label or '',
        description='',
        embedding_model=embedding_model,
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
        joined = "\n\n".join([p.text for p in parsed])
        return joined
