from uuid import uuid4

from pydantic import EmailStr, UUID4

from fai_backend.conversations.models import Conversation
from fai_backend.conversations.schema import (
    CreateConversationRequest,
    FeedbackResponse,
    ResponseMessage,
)
from fai_backend.repositories import ConversationRepository
from fai_backend.repository.query.component import LogicalExpression, AttributeAssignment


class ConversationService:
    conversations_repo: ConversationRepository

    def __init__(self, conversation_repo: ConversationRepository):
        self.conversations_repo = conversation_repo

    async def create_conversation(
            self, user_email: EmailStr, conversation: CreateConversationRequest
    ) -> Conversation | None:
        conversation = Conversation.model_validate({
            **conversation.model_dump(exclude={'messages'}),
            'messages': [{**message.model_dump(), 'user': user_email} for message in conversation.messages],
            'participants': [user_email],
            'created_by': user_email,
            'id': 'temp_id'
        })
        conversation.created_by = user_email
        conversation.participants.append(user_email)
        return Conversation.model_validate((await self.conversations_repo.create(
            Conversation.model_validate(conversation.model_dump(exclude={'id'}))
        )).model_dump())

    @staticmethod
    def get_conversation_copy(conversation: Conversation) -> Conversation:
        conversation_copy = conversation.dict()

        conversation_copy.update({
            'id': str(uuid4()),
            'conversation_id': uuid4(),
            'conversation_root_id': conversation.conversation_id,
            'conversation_active_id': None
        })

        return Conversation.model_validate(conversation_copy)

    async def set_active_conversation(self, conversation_to_activate: Conversation):
        root_id = AttributeAssignment('conversation_id', conversation_to_activate.conversation_root_id)
        root_conversation = (await self.conversations_repo.list(query=root_id))[0]

        new_conversation_active_id = {'conversation_active_id': conversation_to_activate.conversation_id}
        return await self.conversations_repo.update(root_conversation.id, new_conversation_active_id)

    async def add_feedback(self, message, email, body) -> FeedbackResponse | None:
        pass

    async def add_message(self, param, email, body) -> list[ResponseMessage]:
        pass

    async def get_conversation_by_id(
            self, conversation_id: str
    ) -> Conversation | None:
        conversation = await self.conversations_repo.get(conversation_id)
        return Conversation.model_validate(conversation.model_dump()) if conversation else None

    async def list_conversations(self) -> list[Conversation]:
        return [Conversation.model_validate(conversation.model_dump()) for conversation in
                await self.conversations_repo.list()]
