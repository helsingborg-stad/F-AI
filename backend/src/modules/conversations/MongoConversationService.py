import datetime

import pymongo
from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id
from src.modules.conversations.models.Conversation import Conversation
from src.modules.conversations.models.Message import Message
from src.modules.conversations.protocols.IConversationService import IConversationService


class MongoConversationService(IConversationService):
    def __init__(self, database: AsyncDatabase):
        self._database = database

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

    async def add_message_to_conversation(self, as_uid: str, conversation_id: str, message: Message,
                                          restart_from: str | None = None) -> str | None:
        new_message = Message(**message.model_dump(exclude={'id'}), id=str(ObjectId()))

        conversation = await self.get_conversation(as_uid, conversation_id)
        if conversation:
            if restart_from is not None:
                index = next((i for i, m in enumerate(conversation.messages) if m.id == restart_from), None)
                if index is None:
                    return None

                conversation.messages = conversation.messages[0:index] + [new_message]
            else:
                conversation.messages.append(new_message)

            result = await self._database['conversations'].update_one(
                {'_id': ObjectId(conversation_id), 'owner': as_uid},
                {'$set': {'messages': [m.model_dump() for m in conversation.messages]}})

            return new_message.id if result.modified_count == 1 else None

        return None

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
