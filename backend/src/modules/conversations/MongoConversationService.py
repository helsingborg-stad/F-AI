from bson import ObjectId
from pymongo.asynchronous.database import AsyncDatabase

from src.common.mongo import is_valid_mongo_id
from src.modules.conversations.models.Conversation import Conversation
from src.modules.conversations.models.Message import Message
from src.modules.conversations.protocols.IConversationService import IConversationService


class MongoConversationService(IConversationService):
    def __init__(self, database: AsyncDatabase):
        self._database = database

    async def create_conversation(self, assistant_id: str) -> str:
        new_id = ObjectId()
        result = await self._database['conversations'].insert_one(
            {
                '_id': new_id,
                'assistant_id': assistant_id,
                'title': '',
                'messages': []
            }
        )
        return str(result.inserted_id)

    async def get_conversation(self, conversation_id: str) -> Conversation | None:
        if not is_valid_mongo_id(conversation_id):
            return None

        result = await self._database['conversations'].find_one(
            {'_id': ObjectId(conversation_id)},
            projection=['_id', 'assistant_id', 'title', 'messages']
        )
        if result is None:
            return None
        return self._doc_to_conversation(result)

    async def get_conversations(self) -> list[Conversation]:
        cursor = self._database['conversations'].find(projection=['_id', 'assistant_id', 'title', 'messages'])
        return [self._doc_to_conversation(doc) async for doc in cursor]

    async def add_message_to_conversation(self, conversation_id: str, timestamp: str, role: str, message: str) -> bool:
        conversation = await self.get_conversation(conversation_id)
        if conversation:
            conversation.messages.append(Message(
                timestamp=timestamp,
                role=role,
                content=message
            ))
            await self._database['conversations'].update_one({'_id': ObjectId(conversation_id)},
                                                             {'$set': {**conversation.model_dump(exclude={'id'})}})
            return True
        return False

    async def add_to_conversation_last_message(
            self,
            conversation_id: str,
            timestamp: str,
            role: str,
            additional_message: str
    ) -> bool:
        conversation = await self.get_conversation(conversation_id)

        if not conversation:
            return False

        if len(conversation.messages) == 0:
            await self.add_message_to_conversation(conversation_id, timestamp, role, additional_message)
            return True

        conversation.messages[-1].timestamp = timestamp
        conversation.messages[-1].role = role
        conversation.messages[-1].content = conversation.messages[-1].content + additional_message
        result = await self._database['conversations'].update_one({'_id': ObjectId(conversation_id)}, {
            "$set": {
                'messages': conversation.model_dump(include={'messages'})['messages']
            }
        })
        return result.modified_count == 1

    async def set_conversation_title(self, conversation_id: str, title: str) -> bool:
        if not is_valid_mongo_id(conversation_id):
            return False
        result = await self._database['conversations'].update_one({'_id': ObjectId(conversation_id)},
                                                                  {'$set': {'title': title}})
        return result.modified_count == 1

    async def delete_conversation(self, conversation_id: str):
        await self._database['conversations'].delete_one({'_id': ObjectId(conversation_id)})

    @staticmethod
    def _doc_to_conversation(doc):
        return Conversation(
            id=str(doc['_id']),
            assistant_id=doc['assistant_id'],
            title=doc['title'],
            messages=[
                Message(timestamp=m['timestamp'], role=m['role'], content=m['content'])
                for m in doc['messages']
            ])
