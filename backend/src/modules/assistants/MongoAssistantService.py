from typing import Mapping, Any

from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id
from src.modules.assistants.models.Assistant import Assistant
from src.modules.assistants.models.AssistantMeta import AssistantMeta
from src.modules.assistants.protocols.IAssistantService import IAssistantService


class MongoAssistantService(IAssistantService):
    def __init__(self, database: AsyncDatabase):
        self._database = database

    async def create_assistant(self) -> str:
        assistant = Assistant(
            id=str(ObjectId()),
            meta=AssistantMeta(name='', description='', sample_questions=[]),
            model='',
            llm_api_key=None,
            instructions='',
            temperature=1,
            max_tokens=16000,
            allow_files=False,
            collection_id=None
        )
        result = await self._database['assistants'].insert_one({
            **assistant.model_dump(exclude={'id'}),
            '_id': ObjectId(assistant.id),
        })
        return str(result.inserted_id)

    async def get_assistant(self, assistant_id: str) -> Assistant | None:
        if not is_valid_mongo_id(assistant_id):
            return None

        doc = await self._database['assistants'].find_one(
            {'_id': ObjectId(assistant_id)},
            projection=[
                '_id',
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

        return self._doc_to_assistant(doc)

    async def get_assistants(self) -> list[Assistant]:
        cursor = self._database['assistants'].find(
            projection=[
                '_id',
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
        return [self._doc_to_assistant(doc) async for doc in cursor]

    async def update_assistant(
            self,
            assistant_id: str,
            name: str,
            description: str,
            sample_questions: list[str],
            model: str,
            llm_api_key: str | None,
            instructions: str,
            temperature: float,
            max_tokens: int,
            allow_files: bool,
            collection_id: str,
    ) -> bool:
        if not is_valid_mongo_id(assistant_id):
            return False

        result = await self._database['assistants'].update_one(
            {'_id': ObjectId(assistant_id)},
            {
                '$set': {
                    'meta': {
                        'name': name,
                        'description': description,
                        'sample_questions': sample_questions,
                    },
                    'model': model,
                    'llm_api_key': llm_api_key,
                    'instructions': instructions,
                    'temperature': temperature,
                    'max_tokens': max_tokens,
                    'allow_files': allow_files,
                    'collection_id': collection_id,
                }
            }
        )

        return result.modified_count == 1

    async def delete_assistant(self, assistant_id: str) -> None:
        if not is_valid_mongo_id(assistant_id):
            return None
        await self._database['assistants'].delete_one({'_id': ObjectId(assistant_id)})

    @staticmethod
    def _doc_to_assistant(doc: Mapping[str, Any]) -> Assistant:
        return Assistant(
            id=str(doc['_id']),
            meta=AssistantMeta(
                name=doc['meta']['name'],
                description=doc['meta']['description'],
                sample_questions=doc['meta']['sample_questions']
            ),
            model=doc['model'],
            llm_api_key=doc['llm_api_key'],
            instructions=doc['instructions'],
            temperature=doc['temperature'],
            max_tokens=doc['max_tokens'],
            allow_files=doc['allow_files'],
            collection_id=doc['collection_id']
        )
