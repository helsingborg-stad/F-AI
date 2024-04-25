from fastapi import APIRouter, Depends, UploadFile

from fai_backend.dependencies import get_page_template_for_logged_in_users, get_project_user
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.service import FileUploadService
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.phrase import phrase as _
from fai_backend.schema import ProjectUser

router = APIRouter(
    prefix='/api',
    tags=['Documents'],
    route_class=LoggingAPIRouter,
)


@router.get('/documents', response_model=list, response_model_exclude_none=True)
def list_view(
        file_service: FileUploadService = Depends(get_file_upload_service),
        project_user: ProjectUser = Depends(get_project_user),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    documents = file_service.list_files(project_user.project_id)
    return view(
        c.Div(components=[
            c.Div(components=[
                c.Table(
                    data=[
                        {
                            'file_name': document.file_name,
                            'file_size': document.file_size.human_readable(),
                            'mime_type': document.mime_type,
                            'upload_date': document.upload_date.date(),
                        }
                        for document in documents
                    ],
                    columns=[
                        {'key': 'file_name', 'label': _('file_name', 'File name')},
                        {'key': 'file_size', 'label': _('file_size', 'File size')},
                        {'key': 'mime_type', 'label': _('mime_type', 'Mime type')},
                        {'key': 'upload_date', 'label': _('upload_date', 'Upload date')},
                    ],

                    class_name='text-base-content join-item md:table-sm lg:table-md table-auto',
                ),
            ], class_name='overflow-x-auto space-y-4'),
        ], class_name='card bg-base-100 w-full max-w-6xl'),
        _('documents', 'Documents'),
    )


@router.get('/documents/upload', response_model=list, response_model_exclude_none=True)
def upload_view(
        project_user: ProjectUser = Depends(get_project_user),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    return view(
        c.Form(
            submit_as='form',
            submit_url='/api/documents/upload',
            components=[
                c.FileInput(
                    name='files',
                    title=_('file', 'File'),
                    required=True,
                    multiple=True,
                ),
                c.Button(
                    html_type='submit',
                    label=_('upload', 'Upload'),
                    class_name='btn btn-primary',
                ),
            ],
            class_name='card bg-base-100 w-full max-w-6xl',
        ),
        _('upload_documents', 'Upload documents'),
    )


@router.post('/documents/upload', response_model=list, response_model_exclude_none=True)
def upload_handler(
        files: list[UploadFile],
        project_user: ProjectUser = Depends(get_project_user),
        file_service: FileUploadService = Depends(get_file_upload_service),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    file_service.save_files(project_user.project_id, files)

    return view(
        c.FireEvent(event=e.GoToEvent(url='/documents')),
        _('submit_a_question', 'Create Question'''),
    )


@router.post('documents/parse_and_save', response_model=list, response_model_exclude_none=True)
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
