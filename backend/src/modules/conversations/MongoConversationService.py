import datetime
import os
import time

import pymongo
from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.conversations.models.Conversation import Conversation
from src.modules.conversations.models.Message import Message
from src.modules.conversations.protocols.IConversationService import IConversationService
from src.modules.metrics.models.Metric import Metric, MetricValue
from src.modules.metrics.protocols.IMetricsProvider import IMetricsProvider


class MongoConversationService(IConversationService, IMetricsProvider):
    def __init__(self, database: AsyncDatabase, assistant_service: IAssistantService):
        self._database = database
        self._assistant_service = assistant_service

    async def create_conversation(self, as_uid: str, assistant_id: str) -> str:
        new_id = ObjectId()
        result = await self._database['conversations'].insert_one(
            {
                '_id': new_id,
                'created_at': datetime.datetime.utcnow(),
                'owner': as_uid,
                'assistant_id': assistant_id,
                'title': '',
                'messages': []
            }
        )

        return str(result.inserted_id)

    async def get_conversation(self, as_uid: str, conversation_id: str) -> Conversation | None:
        if not is_valid_mongo_id(conversation_id):
            return None

        result = await self._database['conversations'].find_one(
            {'_id': ObjectId(conversation_id), 'owner': as_uid},
            projection=['_id', 'assistant_id', 'title', 'messages']
        )

        return self._doc_to_conversation(result) if result else None

    async def get_conversations(self, as_uid: str) -> list[Conversation]:
        cursor = self._database['conversations'].find(
            {'owner': as_uid},
            projection=['_id', 'assistant_id', 'title', 'messages']
        ).sort('created_at', pymongo.DESCENDING)

        return [self._doc_to_conversation(doc) async for doc in cursor]

    async def add_message_to_conversation(self, as_uid: str, conversation_id: str, message: Message) -> bool:
        conversation = await self.get_conversation(as_uid, conversation_id)
        if conversation:
            conversation.messages.append(message)

            result = await self._database['conversations'].update_one(
                {'_id': ObjectId(conversation_id), 'owner': as_uid},
                {'$set': {'messages': [m.model_dump() for m in conversation.messages]}})

            return result.modified_count == 1

        return False

    async def replace_conversation_last_message(self, as_uid: str, conversation_id: str, message: Message) -> bool:
        conversation = await self.get_conversation(as_uid, conversation_id)

        if not conversation or len(conversation.messages) == 0:
            return False

        conversation.messages[-1] = message

        result = await self._database['conversations'].update_one(
            {'_id': ObjectId(conversation_id), 'owner': as_uid},
            {"$set": {'messages': conversation.model_dump(include={'messages'})['messages']}}
        )
        return result.modified_count == 1

    async def set_conversation_title(self, as_uid: str, conversation_id: str, title: str) -> bool:
        if not is_valid_mongo_id(conversation_id):
            return False
        result = await self._database['conversations'].update_one(
            {'_id': ObjectId(conversation_id), 'owner': as_uid},
            {'$set': {'title': title}})
        return result.modified_count == 1

    async def delete_conversation(self, as_uid: str, conversation_id: str):
        if not is_valid_mongo_id(conversation_id):
            return
        await self._database['conversations'].delete_one(
            {'_id': ObjectId(conversation_id), 'owner': as_uid}
        )

    @staticmethod
    def _doc_to_conversation(doc):
        title = doc['title']

        if len(title) == 0:
            first_user_message = next((m['content'] for m in doc['messages'] if m['role'] == 'user'), None)
            if first_user_message:
                title = first_user_message

        return Conversation(
            id=str(doc['_id']),
            assistant_id=doc['assistant_id'],
            title=title,
            messages=[
                Message(**m)
                for m in doc['messages']
            ])

    async def get_metrics(self) -> list[Metric]:
        assistant_count_result = await self._database['conversations'].aggregate([
            {"$group": {
                "_id": "$assistant_id",
                "count": {"$sum": 1}
            }},
        ])

        assistant_counts = await assistant_count_result.to_list()

        assistant_name_cache = {}
        for assistant_count in assistant_counts:
            if assistant_count['_id'] not in assistant_name_cache:
                info = await self._assistant_service.get_assistant_info(as_uid=os.environ['SETUP_ADMIN'],
                                                                        assistant_id=assistant_count['_id'])
                if info:
                    assistant_name_cache[assistant_count['_id']] = info.meta['name'] if 'name' in info.meta else \
                    assistant_count['_id']
            assistant_count['name'] = assistant_name_cache[assistant_count['_id']] if assistant_count[
                                                                                          '_id'] in assistant_name_cache else \
            assistant_count['_id']

        return [Metric(
            name='conversation_count',
            help='Number of conversations per assistant',
            type='gauge',
            values=[MetricValue(
                timestamp_s=int(time.time()),
                value=assistant_count['count'],
                attributes={"assistant": assistant_count['name'].replace('"', '\\"')})
                for assistant_count in assistant_counts
            ]
        )]
