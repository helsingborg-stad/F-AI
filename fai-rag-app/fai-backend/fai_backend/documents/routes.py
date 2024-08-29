from fastapi import APIRouter, Depends, UploadFile

from fai_backend.config import settings
from fai_backend.dependencies import get_page_template_for_logged_in_users, get_project_user
from fai_backend.files.dependecies import get_file_upload_service
from fai_backend.files.service import FileUploadService
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter
from fai_backend.message_broker.dependencies import get_message_queue
from fai_backend.message_broker.interface import IMessageQueue
from fai_backend.phrase import phrase as _
from fai_backend.projects.dependencies import list_projects_request, update_project_request, get_project_service
from fai_backend.projects.schema import ProjectResponse, ProjectUpdateRequest
from fai_backend.projects.service import ProjectService
from fai_backend.schema import ProjectUser
from fai_backend.vector.schema import VectorizeFilesModel

router = APIRouter(
    prefix='/api',
    tags=['Documents'],
    route_class=LoggingAPIRouter,
)


@router.get('/view/documents', response_model=list, response_model_exclude_none=True)
def list_view(
        file_service: FileUploadService = Depends(get_file_upload_service),
        project_user: ProjectUser = Depends(get_project_user),
        view=Depends(get_page_template_for_logged_in_users),
) -> list:
    files = file_service.list_files(project_user.project_id)
    most_recent_collection = max(files, key=lambda file: file.upload_date).collection if files else []
    most_recent_upload_files = [file for file in files if file.collection == most_recent_collection]

    return view(
        c.Div(components=[
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
        _('documents', 'Documents'),
    )


@router.get('/view/documents/upload_form', response_model=list, response_model_exclude_none=True)
def upload_view(view=Depends(get_page_template_for_logged_in_users)) -> list:
    return view(
        c.Form(
            submit_as='form',
            submit_url='/api/documents/upload_files',
            components=[
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
        _('upload_documents', 'Upload documents'),
    )


@router.post('/documents/upload_files', response_model=list, response_model_exclude_none=True)
async def upload_files_handler(files: list[UploadFile],
                               project_user: ProjectUser = Depends(get_project_user),
                               message_queue: IMessageQueue = Depends(get_message_queue),
                               file_service: FileUploadService = Depends(get_file_upload_service),
                               view=Depends(get_page_template_for_logged_in_users),
                               projects: list[ProjectResponse] = Depends(list_projects_request),
                               project_service: ProjectService = Depends(get_project_service)) -> list:
    project_id = project_user.project_id
    upload_path = file_service.save_files(project_id, files)
    message_queue.enqueue(settings.APP_MESSAGE_BROKER_TASK_FUNC,
                          base_url=settings.APP_MESSAGE_BROKER_BASE_URL,
                          task_id=project_id,
                          path='api/vector/vectorize_files',
                          data=VectorizeFilesModel(directory_path=upload_path).model_dump())

    # Fix/workaround for updating assistant file collection id
    # until assistant editor ui is done
    upload_directory_name = upload_path.split('/')[-1]
    for project in projects:
        for assistant in project.assistants:
            if assistant.files_collection_id is not None:
                assistant.files_collection_id = upload_directory_name
                await update_project_request(body=ProjectUpdateRequest(**project.model_dump()),
                                             existing_project=project,
                                             project_service=project_service)

    return view(c.FireEvent(event=e.GoToEvent(url='/view/documents')),
                _('submit_a_question', 'Create Question'))
