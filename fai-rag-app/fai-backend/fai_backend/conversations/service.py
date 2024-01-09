from typing import Optional

from pydantic import EmailStr

from fai_backend.conversations.schema import (
    RequestConversation,
    ResponseConversation,
    ResponseFeedback,
    ResponseMessage,
)
from fai_backend.repositories import ConversationRepository


class ConversationService:
    conversations_repo: ConversationRepository

    def __init__(self, conversation_repo: ConversationRepository):
        self.conversations_repo = conversation_repo

    async def create_conversation(
            self, user_email: EmailStr, body: RequestConversation
    ) -> ResponseConversation:
        pass

    async def add_feedback(self, message, email, body) -> Optional[ResponseFeedback]:
        pass

    async def add_message(self, param, email, body) -> list[ResponseMessage]:
        pass

    async def get_conversation_by_id(
            self, conversation_id
    ) -> Optional[ResponseConversation]:
        pass

    async def list_conversations(self) -> list[ResponseConversation]:
        pass
