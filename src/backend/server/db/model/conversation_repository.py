from backend.server.db.model.conversation import (
    ConversationModel,
    InsertConversationModel,
    InsertFeedbackModel,
)


from abc import ABC, abstractmethod
from typing import Any, Dict, List


class ConversationRepositoryModel(ABC):
    @abstractmethod
    async def insert(self, input: InsertConversationModel) -> ConversationModel:
        raise NotImplementedError()

    @abstractmethod
    async def find_by_id(
        self,
        q: Dict[str, Any] = {},
    ) -> List[ConversationModel]:
        raise NotImplementedError()

    @abstractmethod
    async def find_all(
        self,
        q: Dict[str, Any] = {},
    ) -> List[ConversationModel]:
        raise NotImplementedError()

    @abstractmethod
    async def insert_message(
        self, messages: List[Dict[str, Any],]
    ) -> ConversationModel:
        raise NotImplementedError()

    @abstractmethod
    async def insert_feedback(
        self,
        conversation_id: str,
        message_index: int,
        feedback_input: InsertFeedbackModel,
    ) -> ConversationModel:
        raise NotImplementedError()
