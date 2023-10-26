

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, UUID4

class TimestampModel(BaseModel):
    created: datetime = Field(default_factory=datetime.now)
    modified: datetime = Field(default_factory=datetime.now)

class FeedbackModel(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None
    timestamp: TimestampModel = TimestampModel()

class MessageModel(BaseModel):
    user: str
    content: str
    feedback: Optional[List[FeedbackModel]] = []
    timestamp: TimestampModel = TimestampModel()

class ConversationModel(BaseModel):
    id: str
    created_by: str
    participants: List[str]
    messages: List[MessageModel]
    timestamp: TimestampModel = TimestampModel()
    
class InsertFeedbackModel(BaseModel):
    user: str
    rating: str
    comment: Optional[str] = None
    
class InsertMessageModel(BaseModel):
    user: str
    content: str
    feedback: Optional[List[FeedbackModel]] = []

class InsertConversationModel(BaseModel):
    created_by: str
    messages: List[InsertMessageModel]
    participants: List[str]

class ConversationRepositoryModel(ABC):
    @abstractmethod
    async def insert(self, input: InsertConversationModel)->ConversationModel:
        raise NotImplementedError()
    
    @abstractmethod
    async def find_by_id(self, q: Dict[str, Any] = {}, )->List[ConversationModel]:
        raise NotImplementedError()
    
    @abstractmethod
    async def find_all(self, q: Dict[str, Any] = {}, )->List[ConversationModel]:
        raise NotImplementedError()
    
    @abstractmethod
    async def insert_message(self, messages: List[Dict[str, Any], ])->ConversationModel:
        raise NotImplementedError()
    
    @abstractmethod
    async def insert_feedback(self, conversation_id: str, message_index: int, feedback_input: InsertFeedbackModel)->ConversationModel:
        raise NotImplementedError()
    

