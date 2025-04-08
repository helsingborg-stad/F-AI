from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator

conversation_router = APIRouter(
    prefix='/conversation',
    tags=['Conversation']
)

auth = AuthRouterDecorator(conversation_router)


class GetConversationsResponseConversation(BaseModel):
    id: str
    timestamp: str
    title: str


class GetConversationsResponse(BaseModel):
    conversations: list[GetConversationsResponseConversation]


@auth.get(
    '',
    ['conversation.read'],
    response_model=GetConversationsResponse,
)
async def get_conversations(services: ServicesDependency):
    result = await services.conversation_service.get_conversations()

    return GetConversationsResponse(conversations=[
        GetConversationsResponseConversation(
            id=conversation.id,
            timestamp=conversation.messages[0].timestamp if len(conversation.messages) > 0 else '',
            title=conversation.title
        ) for conversation in result
    ])


class GetConversationResponseConversationMessage(BaseModel):
    timestamp: str
    role: str
    content: str


class GetConversationResponseConversation(BaseModel):
    title: str
    assistant_id: str
    messages: list[GetConversationResponseConversationMessage]


class GetConversationResponse(BaseModel):
    conversation: GetConversationResponseConversation


@auth.get(
    '/{conversation_id}',
    ['conversation.read'],
    response_model=GetConversationResponse,
    response_404_description='Conversation not found'
)
async def get_conversation(conversation_id: str, services: ServicesDependency):
    result = await services.conversation_service.get_conversation(conversation_id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return GetConversationResponse(conversation=GetConversationResponseConversation(
        title=result.title,
        assistant_id=result.assistant_id,
        messages=[GetConversationResponseConversationMessage(
            timestamp=message.timestamp,
            role=message.role,
            content=message.content
        ) for message in result.messages]
    ))


class SetConversationTitleRequest(BaseModel):
    title: str


@auth.patch(
    '/{conversation_id}/title',
    ['conversation.write'],
    response_404_description='Conversation not found'
)
async def set_conversation_title(conversation_id: str, body: SetConversationTitleRequest, services: ServicesDependency):
    success = await services.conversation_service.set_conversation_title(conversation_id, body.title)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@auth.delete(
    '/{conversation_id}',
    ['conversation.write'],
)
async def delete_conversation(conversation_id: str, services: ServicesDependency):
    await services.conversation_service.delete_conversation(conversation_id)
