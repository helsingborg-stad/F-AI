import base64
from typing import Mapping, Any

import gridfs
from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id
from src.modules.assistants.models.Assistant import Assistant
from src.modules.assistants.models.AssistantInfo import AssistantInfo
from src.modules.assistants.models.AssistantMeta import AssistantMeta
from src.modules.assistants.models.Model import Model
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.resources.protocols.IResourceService import IResourceService


class MongoAssistantService(IAssistantService):
    def __init__(self, database: AsyncDatabase, resource_service: IResourceService):
        self._database = database
        self._resource_service = resource_service

    async def create_assistant(self, as_uid: str, force_id: str | None = None) -> str:
        if force_id and await self._database['assistants'].find_one({'_id': ObjectId(force_id)}) is not None:
            return force_id

        assistant = Assistant(
            id=force_id if force_id else str(ObjectId()),
            owner=as_uid,
            meta=AssistantMeta(name='', description='', avatar_base64='', sample_questions=[], allow_files=False,
                               is_public=False, primary_color='#ffffff'),
            model='',
            llm_api_key=None,
            instructions='',
            collection_id=None,
            extra_llm_params=None
        )
        result = await self._database['assistants'].insert_one({
            **assistant.model_dump(exclude={'id'}),
            '_id': ObjectId(assistant.id)
        })
        return str(result.inserted_id)

    async def get_available_models(self, as_uid: str) -> list[Model]:
        cursor = self._database['chat_models'].find(projection=['key', 'provider', 'display_name', 'description'])
        return [Model(
            key=doc['key'],
            provider=doc['provider'],
            display_name=doc['display_name'],
            description=doc['description']
        ) async for doc in cursor]

    async def set_available_models(self, models: list[Model]) -> bool:
        await self._database['chat_models'].drop()
        if len(models) == 0:
            return True
        result = await self._database['chat_models'].insert_many([
            {
                'key': model.key,
                'provider': model.provider,
                'display_name': model.display_name,
                'description': model.description
            }
            for model in models
        ])
        return len(result.inserted_ids) == len(models)

    async def get_assistant(self, as_uid: str, assistant_id: str, redact_key: bool = True) -> Assistant | None:
        if not is_valid_mongo_id(assistant_id):
            return None

        can_access = await self._resource_service.can_access(as_uid=as_uid, resource=assistant_id)

        doc = await self._database['assistants'].find_one(
            {
                "$and": [
                    {'_id': ObjectId(assistant_id)},
                    {"$or":
                         [{'owner': as_uid}, {"meta.is_public": True}] if not can_access else
                         [{'$or': [{"_id": {"$exists": True}}]}]
                     }
                ]
            },
            projection=[
                '_id',
                'owner',
                'meta',
                'model',
                'llm_api_key',
                'instructions',
                'temperature',
                'max_tokens',
                'allow_files',
                'collection_id',
                'extra_llm_params',
                'response_schema'
            ]
        )
        if doc is None:
            return None

        return await self._doc_to_assistant(doc, redact_key=redact_key)

    async def get_owned_assistants(self, as_uid: str) -> list[Assistant]:
        cursor = self._database['assistants'].find(
            {'owner': as_uid},
            projection=[
                '_id',
                'owner',
                'meta',
                'model',
                'llm_api_key',
                'instructions',
                'temperature',
                'max_tokens',
                'allow_files',
                'collection_id',
                'extra_llm_params',
                'response_schema'
            ]
        )
        return [await self._doc_to_assistant(doc, True) async for doc in cursor]

    async def get_assistant_info(self, as_uid: str, assistant_id: str) -> AssistantInfo | None:
        can_access = await self._resource_service.can_access(as_uid=as_uid, resource=assistant_id)

        doc = await self._database['assistants'].find_one(
            {
                "$and": [
                    {'_id': ObjectId(assistant_id)},
                    {"$or":
                         [{'owner': as_uid}, {"meta.is_public": True}] if not can_access else
                         [{'$or': [{"_id": {"$exists": True}}]}]
                     }
                ]
            },
            projection=[
                '_id',
                'meta',
                'model'
            ]
        )
        if doc is None:
            return None

        return await self._doc_to_assistant_info(doc)

    async def get_available_assistants(self, as_uid: str) -> list[AssistantInfo]:
        resources = await self._resource_service.get_resources(as_uid=as_uid)
        cursor = self._database['assistants'].find(
            {"$or": [
                {'owner': as_uid},
                {'_id': {"$in": [ObjectId(resource) for resource in resources]}},
                {'meta.is_public': True}
            ]},
            projection=['_id', 'meta', 'model']
        )
        return [await self._doc_to_assistant_info(doc) async for doc in cursor]

    async def update_assistant(
            self,
            as_uid: str,
            assistant_id: str,
            name: str | None = None,
            description: str | None = None,
            avatar_base64: str | None = None,
            primary_color: str | None = None,
            allow_files: bool | None = None,
            sample_questions: list[str] | None = None,
            is_public: bool | None = None,
            model: str | None = None,
            llm_api_key: str | None = None,
            instructions: str | None = None,
            collection_id: str | None = None,
            response_schema: dict[str, object] | None = None,
            extra_llm_params: dict[str, float | int | bool | str] | None = None
    ) -> bool:
        if not is_valid_mongo_id(assistant_id):
            return False

        update_dict: dict[str, Any] = {}

        self._add_to_dict_unless_none(update_dict, 'meta.name', name)
        self._add_to_dict_unless_none(update_dict, 'meta.description', description)
        self._add_to_dict_unless_none(update_dict, 'meta.primary_color', primary_color)
        self._add_to_dict_unless_none(update_dict, 'meta.allow_files', allow_files)
        self._add_to_dict_unless_none(update_dict, 'meta.sample_questions', sample_questions)
        self._add_to_dict_unless_none(update_dict, 'meta.is_public', is_public)
        self._add_to_dict_unless_none(update_dict, 'model', model)
        self._add_to_dict_unless_none(update_dict, 'llm_api_key', llm_api_key)
        self._add_to_dict_unless_none(update_dict, 'instructions', instructions)
        self._add_to_dict_unless_none(update_dict, 'extra_llm_params', extra_llm_params)
        self._add_to_dict_unless_none(update_dict, 'collection_id', collection_id)
        self._add_to_dict_unless_none(update_dict, 'response_schema', response_schema)

        result = await self._database['assistants'].update_one(
            {'_id': ObjectId(assistant_id), 'owner': as_uid},
            {
                '$set': {**update_dict}
            }
        )

        if avatar_base64 is not None:
            fs = gridfs.AsyncGridFS(self._database)

            doc = await self._database['assistants'].find_one({'_id': ObjectId(assistant_id), 'owner': as_uid},
                                                              projection=['meta'])

            if doc and 'gfs_avatar' in doc['meta'] and doc['meta']['gfs_avatar'] is not None:
                await fs.delete(doc['meta']['gfs_avatar'])

            if avatar_base64 == '':
                new_id = None
            else:
                decoded = base64.b64decode(avatar_base64)
                new_id = await fs.put(decoded, filename=f'{assistant_id}.png')

            await self._database['assistants'].update_one({'_id': ObjectId(assistant_id), 'owner': as_uid},
                                                          {'$set': {'meta.gfs_avatar': new_id}})

        return result.matched_count == 1

    async def delete_assistant(self, as_uid: str, assistant_id: str) -> None:
        if is_valid_mongo_id(assistant_id):
            await self._database['assistants'].delete_one({'_id': ObjectId(assistant_id), 'owner': as_uid})

    async def set_assistant_as_favorite(self, as_uid: str, assistant_id: str) -> bool:
        resources = await self._resource_service.get_resources(as_uid=as_uid)
        assistant = await self._database['assistants'].find_one(
            {'$and': [
                {'_id': ObjectId(assistant_id)},
                {"$or": [
                    {'owner': as_uid},
                    {'_id': {"$in": [ObjectId(resource) for resource in resources]}},
                    {'meta.is_public': True}
                ]}
            ]},
            projection=['_id']
        )

        if not assistant:
            return False

        result = await self._database['favorite_assistants'].update_one(
            {'_id': as_uid},
            {'$addToSet': {'favorite_assistants': assistant['_id']}},
            upsert=True
        )

        return result.matched_count == 1 or result.upserted_id is not None

    async def get_favorite_assistants(self, as_uid: str) -> list[AssistantInfo]:
        resources = await self._resource_service.get_resources(as_uid=as_uid)
        favorite_list_doc = await self._database['favorite_assistants'].find_one(
            {'_id': as_uid},
            projection=['favorite_assistants']
        )

        raw_favorite_list = [str(aid) for aid in favorite_list_doc['favorite_assistants']] if favorite_list_doc else []

        if len(raw_favorite_list) > 0:
            cursor = self._database['assistants'].find(
                {'$and': [
                    {"$or": [
                        {'owner': as_uid},
                        {'_id': {"$in": [ObjectId(resource) for resource in resources]}},
                        {'meta.is_public': True}
                    ]},
                    {'_id': {"$in": [ObjectId(fid) for fid in raw_favorite_list]}},
                ]},
                projection=['_id', 'meta', 'model']
            )
            return [await self._doc_to_assistant_info(doc) async for doc in cursor]

        return []

    async def remove_assistant_as_favorite(self, as_uid: str, assistant_id: str) -> None:
        await self._database['favorite_assistants'].update_one(
            {'_id': as_uid},
            {'$pull': {'favorite_assistants': ObjectId(assistant_id)}}
        )

    async def _get_avatar_base64(self, file_id: ObjectId | None) -> str | None:
        if file_id is None:
            return None
        fs = gridfs.AsyncGridFS(self._database)
        file = await fs.get(file_id)
        if file is None:
            return None
        return base64.b64encode(await file.read()).decode('utf-8')

    async def _doc_to_assistant(self, doc: Mapping[str, Any], redact_key: bool) -> Assistant:
        api_key = (MongoAssistantService._redact_key(doc['llm_api_key']) if redact_key else doc[
            'llm_api_key']) if 'llm_api_key' in doc else None
        return Assistant(
            id=str(doc['_id']),
            owner=doc['owner'],
            meta=AssistantMeta(
                name=doc['meta']['name'],
                description=doc['meta']['description'],
                avatar_base64=await self._get_avatar_base64(doc['meta']['gfs_avatar']) if 'gfs_avatar' in doc[
                    'meta'] else None,
                allow_files=doc['meta']['allow_files'],
                sample_questions=doc['meta']['sample_questions'],
                is_public=doc['meta']['is_public'] if 'is_public' in doc['meta'] else False,
                primary_color=doc['meta']['primary_color'] if 'primary_color' in doc['meta'] else '#ffffff'
            ),
            model=doc['model'],
            llm_api_key=api_key,
            instructions=doc['instructions'],
            collection_id=doc['collection_id'],
            extra_llm_params=doc['extra_llm_params'] if 'extra_llm_params' in doc else None,
            response_schema=doc['response_schema'] if 'response_schema' in doc else None
        )

    async def _doc_to_assistant_info(self, doc: Mapping[str, Any]) -> AssistantInfo:
        return AssistantInfo(
            id=str(doc['_id']),
            name=doc['meta']['name'],
            description=doc['meta']['description'],
            avatar_base64=await self._get_avatar_base64(doc['meta']['gfs_avatar']) if 'gfs_avatar' in doc[
                'meta'] else None,
            sample_questions=doc['meta']['sample_questions'],
            model=doc['model'],
            primary_color=doc['meta']['primary_color'] if 'primary_color' in doc['meta'] else '#ffffff'
        )

    @staticmethod
    def _add_to_dict_unless_none(in_dict: dict[str, Any], key: str, value: Any | None):
        if value is not None:
            in_dict[key] = value

    @staticmethod
    def _redact_key(key: str) -> str | None:
        return key[:2] + "..." + key[-2:] if key else None
