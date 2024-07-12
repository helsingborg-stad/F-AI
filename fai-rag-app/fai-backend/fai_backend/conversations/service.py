from uuid import uuid4

from bson import ObjectId
from pydantic import EmailStr, UUID4, ValidationError

from fai_backend.conversations.models import Conversation, Message, Feedback
from fai_backend.conversations.schema import (
    CreateConversationRequest,
    FeedbackResponse,
    ResponseMessage,
)
from fai_backend.conversations.utils import get_all_messages_in_conversation
from fai_backend.logger.console import console
from fai_backend.qaf.schema import SubmitAnswerPayload, GenerateAnswerPayload, QuestionFilterParams
from fai_backend.repositories import ConversationRepository
from fai_backend.repository.query.component import LogicalExpression, AttributeAssignment
from fai_backend.schema import ProjectUser


class ConversationService:
    conversations_repo: ConversationRepository

    def __init__(self, conversation_repo: ConversationRepository):
        self.conversations_repo = conversation_repo

    async def create_conversation(
            self, user_email: EmailStr, conversation: CreateConversationRequest
    ) -> Conversation | None:
        conversation_data = conversation.dict(by_alias=True)
        conversation_data.update({
            'participants': [user_email],
            'created_by': user_email
        })

        validated_conversation = Conversation(**conversation_data)

        created_conversation = await self.conversations_repo.create(validated_conversation)
        return created_conversation

    async def add_message_to_conversation(
            self,
            project_user: ProjectUser,
            payload: SubmitAnswerPayload | GenerateAnswerPayload,
    ):
        try:
            conversation_copy = (await self.conversations_repo.get(payload.question_id)).model_copy()
            conversation_messages = get_all_messages_in_conversation(conversation_copy)

            {
                'user': lambda: conversation_messages.append(
                    Message(
                        user='user',
                        content=payload.answer,
                        type='answer',
                        created_by=project_user.email
                    )
                ),
                'assistant': lambda: conversation_messages.append(
                    Message(
                        user='assistant',
                        content=payload.answer,
                        type='generated_answer',
                        created_by=project_user.email
                    )
                )
            }['assistant' if isinstance(payload, GenerateAnswerPayload) else 'user']()

            result = await self.conversations_repo.update(
                conversation_copy
            )

            return result

        except Exception:
            console.print_exception(show_locals=False)

    async def add_feedback(self, message, email, body) -> FeedbackResponse | None:
        pass

    async def add_message(self, param, email, body) -> list[ResponseMessage]:
        pass

    async def update_messages(
            self,
            conversation_id: UUID4,
            messages: list[Message]
    ) -> Conversation:
        return await self.conversations_repo.update(str(conversation_id), {'messages': messages})

    async def update(self, conversation: Conversation) -> Conversation:
        return await self.conversations_repo.update(conversation)

    async def get_conversation_by_id(
            self, conversation_id: str
    ) -> Conversation | None:
        conversation = await self.conversations_repo.get(conversation_id)

        return Conversation.model_validate(conversation) if conversation else None

    async def list_conversations(self) -> list[Conversation]:
        return [Conversation.model_validate(conversation.model_dump()) for conversation in
                await self.conversations_repo.list()]

    async def list_and_sort_conversation(
            self,
            query: LogicalExpression,
            sort_by: str,
            sort_order: str
    ) -> list[Conversation]:
        return await self.conversations_repo.list(query=query, sort_by=sort_by, sort_order=sort_order)

    async def filter_and_list_conversation(
            self,
            query: LogicalExpression,
            query_params: QuestionFilterParams
    ) -> list[Conversation]:
        query_result = await self.conversations_repo.list(
            query=query,
            sort_by=query_params.sort,
            sort_order=query_params.sort_order
        )

        return query_result

    async def create_inactive_copy_of_conversation(
            self,
            conversation_id: str
    ) -> Conversation:
        conversation = await self.conversations_repo.get(conversation_id)

        conversation_data = conversation.dict(by_alias=True)
        conversation_data.update({
            '_id': ObjectId(),
            'conversation_id': uuid4(),
            'conversation_root_id': conversation.conversation_id,
        })
        validated_conversation = Conversation(**conversation_data)

        created_conversation = await self.conversations_repo.create(validated_conversation)
        return created_conversation

    async def set_active_conversation(
            self,
            conversation_id: str
    ) -> Conversation:
        new_active_conversation = await self.conversations_repo.get(conversation_id)

        query = LogicalExpression('AND', [
            AttributeAssignment('conversation_id', new_active_conversation.conversation_root_id),
        ])
        root_conversation = (await self.conversations_repo.list(query=query))[0]

        root_conversation.conversation_active_id = new_active_conversation.conversation_id

        updated_conversation = await self.conversations_repo.update(root_conversation)
        return Conversation.model_validate(updated_conversation.model_dump())
