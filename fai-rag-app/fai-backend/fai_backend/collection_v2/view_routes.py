from datetime import datetime

from fastapi import Depends, APIRouter, UploadFile
from pydantic import ByteSize

from fai_backend.collection.models import CollectionMetadataModel, CollectionFile
from fai_backend.collection_v2.dependencies import get_collection_service
from fai_backend.collection_v2.routes import UpdateCollectionRequest, update_collection, delete_collection, \
    set_collection_files, CreateCollectionRequest, create_collection
from fai_backend.config import settings
from fai_backend.dependencies import get_page_template_for_logged_in_users, get_project_user
from fai_backend.framework.display import DisplayAs
from fai_backend.framework.table import DataColumn
from fai_backend.phrase import phrase as _
from fai_backend.framework import components as c
from fai_backend.framework import events as e
from fai_backend.schema import ProjectUser

router = APIRouter(
    prefix='/api/view',
    tags=['Collections'],
)


class CollectionViewItem(CollectionMetadataModel):
    delete_label: str = "Delete"  # TODO: Hacky


@router.get('/collections', response_model=list, response_model_exclude_none=True)
async def get_collections_view(view=Depends(get_page_template_for_logged_in_users)):
    service = await get_collection_service()
    all_collections = await service.get_collections()
    all_collections = [CollectionViewItem(**col.model_dump()) for col in all_collections]
    return view(
        [
            c.DataTable(
                data=all_collections,
                columns=[
                    DataColumn(
                        key='label',
                        id='label',
                        label='Name',
                    ),
                    DataColumn(
                        key='collection_id',
                        id='collection_id',
                        label='ID',
                        display=DisplayAs.link,
                        on_click=e.GoToEvent(url='/view/collections/{collection_id}'),
                    ),
                    DataColumn(
                        key='description',
                        id='description',
                        label='Description',
                    ),
                    DataColumn(
                        key='delete_label',
                        id='delete',
                        label='Delete',
                        display=DisplayAs.link,
                        on_click=e.GoToEvent(url='/view/collections/{collection_id}/delete'),
                    )
                ],
                include_view_action=False
            )
        ],
        _('collections', 'Collections')
    )


@router.get('/collections/create', response_model=list, response_model_exclude_none=True)
async def get_create_collection_view(view=Depends(get_page_template_for_logged_in_users)):
    return view(
        [
            c.Div(components=get_collection_metadata_form(None, '/api/view/collections'))
        ],
        _('Create Collection')
    )


@router.get('/collections/{collection_id}', response_model=list, response_model_exclude_none=True)
async def get_collection_view(collection_id, view=Depends(get_page_template_for_logged_in_users)):
    service = await get_collection_service()
    collection = await service.get_collection(collection_id)
    if not collection:
        return [c.FireEvent(event=e.GoToEvent(url='/view/collections'))]
    return view(
        [
            c.Div(components=get_collection_metadata_form(collection,
                                                          f'/api/view/collections/{collection_id}'))
        ],
        _('collection', 'Collection')
    )


def get_collection_metadata_form(collection: CollectionMetadataModel | None, submit_url: str):
    return [c.Div(components=[
        c.Div(components=[
            c.Text(text=f'Editing collection {collection.collection_id}' if collection else 'Create new collection'),
            c.Form(
                id=f'assistant-form-{collection.id}' if collection else 'assistant-form',
                submit_url=submit_url,
                method='POST',
                submit_text=_('create_question_submit_button', 'Submit'),
                components=[
                    c.InputField(
                        name='label',
                        label=_('Name'),
                        placeholder=_('Name'),
                        required=True,
                        html_type='text',
                        size='sm',
                        value=collection.label if collection else '',
                    ),
                    c.InputField(
                        name='description',
                        label=_('Description'),
                        placeholder=_('Description'),
                        required=False,
                        html_type='text',
                        size='sm',
                        value=collection.description if collection else '',
                    ),
                    c.Select(
                        name='embedding_model',
                        label=_('Embedding model'),
                        placeholder=_('Select embedding model'),
                        required=True,
                        options=[
                            ('default', 'Default'),
                            ('text-embedding-3-small', 'text-embedding-3-small')
                        ],
                        value=collection.embedding_model if collection else 'default',
                        size='sm',
                    ),
                    *([c.Div(
                        components=[
                            c.Link(
                                text=_('Edit Documents/URLs'),
                                url=f'/view/collections/{collection.collection_id}/files',
                                state='primary'
                            )
                        ]
                    )] if collection else []),
                ],
            )
        ], class_name='card-body'),
    ], class_name='card')]


class CollectionFileViewItem(CollectionFile):
    friendly_byte_size: str
    friendly_timestamp: str


@router.get('/collections/{collection_id}/files', response_model=list, response_model_exclude_none=True)
async def get_collection_files_view(collection_id, view=Depends(get_page_template_for_logged_in_users)):
    service = await get_collection_service()
    collection = await service.get_collection(collection_id)
    if not collection:
        return [c.FireEvent(event=e.GoToEvent(url='/view/collections'))]

    def to_friendly_bytes(byte_size: int) -> str:
        return ByteSize(byte_size).human_readable()

    def to_friendly_timestamp(timestamp: str) -> str:
        return datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')

    viewable_files = [
        CollectionFileViewItem(
            **f.model_dump(),
            friendly_byte_size=to_friendly_bytes(f.byte_size),
            friendly_timestamp=to_friendly_timestamp(f.upload_timestamp)
        ) for f in collection.files]

    return view(
        [
            c.Div(
                components=[
                    c.Text(text=f'Showing content for collection "{collection.label}"'),
                    c.Heading(text='Replace existing content', level=1, class_name='my-5 font-bold'),
                    c.Form(
                        submit_as='form',
                        submit_url=f'/api/view/collections/{collection_id}/files',
                        components=[
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
                                label=_('replace', 'Replace'),
                                class_name='btn btn-primary',
                            ),
                        ],
                        class_name='card-body',
                    ),
                    c.Heading(text='Current content', level=1, class_name='mt-5 font-bold'),
                    c.Heading(text='URLs', level=2, class_name=' mt-2 font-bold'),
                    c.Table(
                        data=[{'url': url} for url in collection.urls] if collection.urls else [],
                        columns=[
                            {'key': 'url', 'label': 'URL'}
                        ]
                    ),
                    c.Heading(text='Files', level=2, class_name='mt-2 font-bold'),
                    c.DataTable(
                        data=viewable_files,
                        columns=[
                            DataColumn(
                                key='name',
                                id='name',
                                label='Name',
                            ),
                            DataColumn(
                                key='friendly_timestamp',
                                id='friendly_timestamp',
                                label='Timestamp',
                            ),
                            DataColumn(
                                key='friendly_byte_size',
                                id='friendly_byte_size',
                                label='Size',
                            )
                        ],
                        include_view_action=False
                    )
                ],
                class_name='card-body',
            )
        ]
        ,
        _('collection content', 'Collection Content')
    )


# WRAPPER ENDPOINTS FOR FRONTEND

@router.post(
    '/collections',
    summary='Create a new collection (called from views)',
    response_model=list,
    response_model_exclude_none=True
)
async def create_collection_from_view(
        data: CreateCollectionRequest,
        view=Depends(get_page_template_for_logged_in_users)
):
    result = await create_collection(data)
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/view/collections/{result.id}'))],
        _('')
    )


@router.post(
    '/collections/{collection_id}',
    summary='Update a collection (called from views)',
    response_model=list,
    response_model_exclude_none=True
)
async def update_collection_from_view(
        collection_id: str,
        data: UpdateCollectionRequest,
        view=Depends(get_page_template_for_logged_in_users)
):
    await update_collection(collection_id, data)
    return view(
        [c.FireEvent(event=e.GoToEvent(url='/view/collections/'))],
        _('')
    )


@router.post(
    '/collections/{collection_id}/files',
    summary='Replace collection files/URLs (called from views)',
    response_model=list,
    response_model_exclude_none=True
)
async def replace_collection_files_from_view(
        collection_id: str,
        files: list[UploadFile] = None,
        urls: list[str] = None,
        view=Depends(get_page_template_for_logged_in_users),
        project_user: ProjectUser = Depends(get_project_user)
):
    await set_collection_files(
        collection_id,
        files,
        urls,
        project_user
    )
    return view(
        [c.FireEvent(event=e.GoToEvent(url=f'/view/collections/{collection_id}/files'))],
        _('')
    )


@router.get(
    '/collections/{collection_id}/delete',
    summary='Delete a collection (called from views)',
    response_model=list,
    response_model_exclude_none=True
)
async def delete_collection_from_view(
        collection_id: str,
        view=Depends(get_page_template_for_logged_in_users),
):
    await delete_collection(collection_id)
    return view(
        [c.FireEvent(event=e.GoToEvent(url='/view/collections/'))],
        _('')
    )
