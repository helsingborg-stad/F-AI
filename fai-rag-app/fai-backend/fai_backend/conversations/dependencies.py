from fastapi import Depends, HTTPException

from fai_backend.conversations.schema import (
    RequestConversation,
    RequestFeedback,
    RequestMessage,
    ResponseConversation,
    ResponseFeedback,
    ResponseMessage,
)
from fai_backend.conversations.service import ConversationService
from fai_backend.dependencies import get_authenticated_user
from fai_backend.repositories import conversation_repo
from fai_backend.schema import User


async def get_conversation_service() -> ConversationService:
    return ConversationService(conversation_repo=conversation_repo)


async def list_conversations_request(
        service: ConversationService = Depends(get_conversation_service),
) -> list[ResponseConversation]:
    conversations = await service.list_conversations() or []
    return [
        ResponseConversation.model_validate(conversation.model_dump())
        for conversation in conversations
    ]


async def get_conversation_request(
        conversation_id: str,
        service: ConversationService = Depends(get_conversation_service),
) -> ResponseConversation:
    conversation = await service.get_conversation_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail='Conversation not found')
    return conversation


async def get_message_request(
        conversation=Depends(get_conversation_request),
        message_id: str = '',
) -> ResponseConversation:
    message = conversation.messages.get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail='Message not found')
    return message


async def create_conversation_request(
        body: RequestConversation,
        user: User = Depends(get_authenticated_user),
        service: ConversationService = Depends(get_conversation_service),
) -> ResponseConversation:
    return await service.create_conversation(user.email, body)


async def add_message_request(
        body: RequestMessage,
        conversation=Depends(get_conversation_request),
        user: User = Depends(get_authenticated_user),
        service: ConversationService = Depends(get_conversation_service),
) -> list[ResponseMessage]:
    return await service.add_message(str(conversation.id), user.email, body)


async def add_feedback_request(
        body: RequestFeedback,
        message: ResponseMessage = Depends(get_message_request),
        user: User = Depends(get_authenticated_user),
        service: ConversationService = Depends(get_conversation_service),
) -> ResponseFeedback:
    return await service.add_feedback(message, user.email, body)
