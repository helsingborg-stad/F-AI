from typing import Mapping, Any

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id
from src.modules.assistants.models.Assistant import Assistant
from src.modules.assistants.models.AssistantMeta import AssistantMeta
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.resources.protocols.IResourceService import IResourceService


class MongoAssistantService(IAssistantService):
    def __init__(self, database: AsyncDatabase, resource_service: IResourceService):
        self._database = database
        self._resource_service = resource_service

    async def create_assistant(self, as_uid: str) -> str:
        assistant = Assistant(
            id=str(ObjectId()),
            owner=as_uid,
            meta=AssistantMeta(name='', description='', sample_questions=[], allow_files=False),
            model='',
            llm_api_key=None,
            instructions='',
            temperature=1,
            max_tokens=16000,
            collection_id=None
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
                    {"$or": [{'owner': as_uid}] if not can_access else [{"_id": {"$exists": True}}]}
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
            ]
        )
        if doc is None:
            return None

        return self._doc_to_assistant(doc, redact_key=redact_key)

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
            ]
        )
        return [self._doc_to_assistant(doc, True) async for doc in cursor]

    async def get_available_assistants(self, as_uid: str) -> list[Assistant]:
        resources = await self._resource_service.get_resources(as_uid=as_uid)
        cursor = self._database['assistants'].find(
            {"$or": [
                {'owner': as_uid},
                {'_id': {"$in": [ObjectId(resource) for resource in resources]}},
            ]}
        )
        return [self._doc_to_assistant(doc, True) async for doc in cursor]

    async def update_assistant(
            self,
            as_uid: str,
            assistant_id: str,
            name: str | None = None,
            description: str | None = None,
            allow_files: bool | None = None,
            sample_questions: list[str] | None = None,
            model: str | None = None,
            llm_api_key: str | None = None,
            instructions: str | None = None,
            temperature: float | None = None,
            max_tokens: int | None = None,
            collection_id: str | None = None,
    ) -> bool:
        if not is_valid_mongo_id(assistant_id):
            return False

        update_dict: dict[str, Any] = {}

        self._add_to_dict_unless_none(update_dict, 'meta.name', name)
        self._add_to_dict_unless_none(update_dict, 'meta.description', description)
        self._add_to_dict_unless_none(update_dict, 'meta.allow_files', allow_files)
        self._add_to_dict_unless_none(update_dict, 'meta.sample_questions', sample_questions)
        self._add_to_dict_unless_none(update_dict, 'model', model)
        self._add_to_dict_unless_none(update_dict, 'llm_api_key', llm_api_key)
        self._add_to_dict_unless_none(update_dict, 'instructions', instructions)
        self._add_to_dict_unless_none(update_dict, 'temperature', temperature)
        self._add_to_dict_unless_none(update_dict, 'max_tokens', max_tokens)
        self._add_to_dict_unless_none(update_dict, 'collection_id', collection_id)

        result = await self._database['assistants'].update_one(
            {'_id': ObjectId(assistant_id), 'owner': as_uid},
            {
                '$set': {**update_dict}
            }
        )

        return result.matched_count == 1

    async def delete_assistant(self, as_uid: str, assistant_id: str) -> None:
        if not is_valid_mongo_id(assistant_id):
            return None
        await self._database['assistants'].delete_one({'_id': ObjectId(assistant_id), 'owner': as_uid})

    @staticmethod
    def _doc_to_assistant(doc: Mapping[str, Any], redact_key: bool) -> Assistant:
        return Assistant(
            id=str(doc['_id']),
            owner=doc['owner'],
            meta=AssistantMeta(
                name=doc['meta']['name'],
                description=doc['meta']['description'],
                allow_files=doc['meta']['allow_files'],
                sample_questions=doc['meta']['sample_questions'],
            ),
            model=doc['model'],
            llm_api_key=MongoAssistantService._redact_key(doc['llm_api_key']) if redact_key else doc['llm_api_key'],
            instructions=doc['instructions'],
            temperature=doc['temperature'],
            max_tokens=doc['max_tokens'],
            collection_id=doc['collection_id']
        )

    @staticmethod
    def _add_to_dict_unless_none(in_dict: dict[str, Any], key: str, value: Any | None):
        if value is not None:
            in_dict[key] = value

    @staticmethod
    def _redact_key(key: str) -> str | None:
        return key[:2] + "..." + key[-2:] if key else None
