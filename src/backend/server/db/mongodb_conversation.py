import asyncio
from typing import Any, Dict, List
from uuid import UUID, uuid4
from fastapi import FastAPI
import motor
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, PydanticObjectId, UpdateResponse, init_beanie
from beanie.operators import Exists, Size
from pydantic import BaseModel, Field, UUID4
import pymongo
from datetime import datetime
from .model.conversation import ConversationRepositoryModel, FeedbackModel, InsertConversationModel, InsertFeedbackModel, InsertMessageModel, MessageModel, TimestampModel, ConversationModel

from rich.pretty import pprint

class ConversationCollection(Document, ConversationModel):    
    class Settings:
        name = "conversations"
        indexes = [
            [
                ("id", pymongo.TEXT),
                ("created_by", pymongo.TEXT),
            ],
            [
                ("timestamp.modified", pymongo.DESCENDING),
                ("timestamp.created", pymongo.DESCENDING),
            ]
        ]

class ConversationRepository(ConversationRepositoryModel):      
    async def insert(self, input: InsertConversationModel)->ConversationModel:
        conversation = ConversationCollection.parse_raw(input.json())
        return await ConversationCollection.insert_one(conversation)
    
    async def find_by_id(self, conversation_id: str, q: Dict[str, Any] = {}, )->List[ConversationModel]:
        return await ConversationCollection.get(conversation_id)
    
    async def find_all(self, q: Dict[str, Any] = {})->List[ConversationModel]:
        return await (
            ConversationCollection
                .find(q)
                .sort("-timestamp.modified", "-timestamp.created")
                .to_list()
        )
    
    async def insert_message(self, conversation_id: str, input_messages: List[InsertMessageModel])->ConversationModel:
        messages = [MessageModel.parse_raw(message.json()) for message in input_messages]
        return await (
            ConversationCollection
               .find_one(ConversationCollection.id == PydanticObjectId(conversation_id))
               .update({
                   "$push": {
                        ConversationCollection.messages: {
                            "$each": messages
                        }
                    },
                    "$set": {
                        ConversationCollection.timestamp.modified: datetime.now()
                    }
                }, 
                response_type=UpdateResponse.NEW_DOCUMENT)
            )
        
    
    async def insert_feedback(self, conversation_id: str, message_index: int, feedback_input: InsertFeedbackModel)->ConversationModel:
        feedback_entry = FeedbackModel.parse_raw(feedback_input.json())
        
        return await (
            ConversationCollection
               .find_one(ConversationCollection.id == PydanticObjectId(conversation_id))
               .update({
                   "$push": {
                        ConversationCollection.messages[message_index].feedback: feedback_entry
                    },
                    "$set": {
                        ConversationCollection.timestamp.modified: datetime.now()
                    }
                }, 
                response_type=UpdateResponse.NEW_DOCUMENT)
            )
        


def init_db_on_start(app: FastAPI):
    @app.on_event("startup")
    async def init_db():
        from beanie import init_beanie
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(
            "mongodb://localhost:27017"
        )

        await init_beanie(database=client.fai_db_local, document_models=[ConversationCollection])
    return init_db