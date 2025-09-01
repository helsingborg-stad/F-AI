import base64
from typing import Mapping, Any

import gridfs
from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id
from src.modules.assistants.models.Assistant import Assistant
from src.modules.assistants.models.AssistantInfo import AssistantInfo
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.models.protocols.IModelService import IModelService
from src.modules.resources.protocols.IResourceService import IResourceService


class MongoAssistantService(IAssistantService):
    def __init__(self, database: AsyncDatabase, resource_service: IResourceService, model_service: IModelService):
        self._database = database
        self._resource_service = resource_service
        self._model_service = model_service

    async def create_assistant(self, as_uid: str, force_id: str | None = None) -> str:
        if force_id and await self._database['assistants'].find_one({'_id': ObjectId(force_id)}) is not None:
            return force_id

        assistant = Assistant(
            id=force_id if force_id else str(ObjectId()),
            owner=as_uid,
            meta={},
            model='',
            llm_api_key=None,
            instructions='',
            collection_id=None,
            max_collection_results=10,
            extra_llm_params=None
        )
        result = await self._database['assistants'].insert_one({
            **assistant.model_dump(exclude={'id'}),
            '_id': ObjectId(assistant.id)
        })
        return str(result.inserted_id)

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
                'max_collection_results',
                'extra_llm_params'
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
                'max_collection_results',
                'extra_llm_params'
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
            meta: dict[str, Any] | None = None,
            is_public: bool | None = None,
            model: str | None = None,
            llm_api_key: str | None = None,
            instructions: str | None = None,
            collection_id: str | None = None,
            max_collection_results: int | None = None,
            extra_llm_params: dict | None = None,
    ) -> bool:
        if not is_valid_mongo_id(assistant_id):
            return False

        update_dict: dict[str, Any] = {}

        if meta and 'avatar_base64' in meta:
            fs = gridfs.AsyncGridFS(self._database)
            doc = await self._database['assistants'].find_one({'_id': ObjectId(assistant_id), 'owner': as_uid},
                                                              projection=['meta'])

            if doc and 'gfs_avatar' in doc['meta'] and doc['meta']['gfs_avatar'] is not None:
                await fs.delete(doc['meta']['gfs_avatar'])

            in_value = meta['avatar_base64']
            del meta['avatar_base64']
            meta['gfs_avatar'] = None

            if isinstance(in_value, str) and len(in_value) > 0:
                decoded = base64.b64decode(in_value)
                new_id = await fs.put(decoded, filename=f'{assistant_id}.png')
                meta['gfs_avatar'] = new_id

        meta_unsets = [f'meta.{k}' for k, v in meta.items() if v is None] if meta else []

        if meta is not None:
            for k, v in meta.items():
                if v is not None:
                    self._add_to_dict_unless_none(update_dict, f'meta.{k}', v)

        self._add_to_dict_unless_none(update_dict, 'meta.is_public', is_public)
        self._add_to_dict_unless_none(update_dict, 'model', model)
        self._add_to_dict_unless_none(update_dict, 'llm_api_key', llm_api_key)
        self._add_to_dict_unless_none(update_dict, 'instructions', instructions)
        self._add_to_dict_unless_none(update_dict, 'extra_llm_params', extra_llm_params)
        self._add_to_dict_unless_none(update_dict, 'collection_id', collection_id)
        self._add_to_dict_unless_none(update_dict, 'max_collection_results', max_collection_results)

        result = await self._database['assistants'].update_one(
            {'_id': ObjectId(assistant_id), 'owner': as_uid},
            {
                '$set': {**update_dict},
                '$unset': {**dict.fromkeys(meta_unsets, '')}
            }
        )

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

    async def _parse_meta(self, doc: Mapping[str, Any]) -> dict[str, Any]:
        result = {k: v for k, v in doc.items() if k != 'gfs_avatar'}
        if 'gfs_avatar' in doc:
            avatar_base64 = await self._get_avatar_base64(doc['gfs_avatar'])
            if avatar_base64 is not None:
                result['avatar_base64'] = avatar_base64
        return result

    async def _doc_to_assistant(self, doc: Mapping[str, Any], redact_key: bool) -> Assistant:
        api_key = (MongoAssistantService._redact_key(doc['llm_api_key']) if redact_key else doc[
            'llm_api_key']) if 'llm_api_key' in doc else None
        return Assistant(
            id=str(doc['_id']),
            owner=doc['owner'],
            meta=await self._parse_meta(doc['meta']) if 'meta' in doc else {},
            model=doc['model'],
            llm_api_key=api_key,
            instructions=doc['instructions'],
            collection_id=doc['collection_id'],
            max_collection_results=doc['max_collection_results'] if 'max_collection_results' in doc else 10,
            extra_llm_params=doc['extra_llm_params'] if 'extra_llm_params' in doc else None,
        )

    async def _doc_to_assistant_info(self, doc: Mapping[str, Any]) -> AssistantInfo:
        return AssistantInfo(
            id=str(doc['_id']),
            model=doc['model'],
            meta=await self._parse_meta(doc['meta']) if 'meta' in doc else None,
        )

    @staticmethod
    def _add_to_dict_unless_none(in_dict: dict[str, Any], key: str, value: Any | None):
        if value is not None:
            in_dict[key] = value

    @staticmethod
    def _redact_key(key: str) -> str | None:
        return key[:2] + "..." + key[-2:] if key else None
