from typing import Annotated, Any, Dict, List, Union
from fastapi import APIRouter, Depends, Header
from backend.server.schema.conversation.input import InputConversation, InputFeedback, InputMessage
from backend.server.schema.conversation.response import OutputConversation, OutputMessage, OutputFeedback
from backend.server.service.conversation_service import ConversationService, create_conversation_service


router = APIRouter(tags=["/api/v1/conversations"])

@router.put("/conversations/", response_model=OutputConversation)
async def create_conversation(
    input: InputConversation, 
    conversations: Annotated[ConversationService, Depends(create_conversation_service)],
)->OutputConversation:
    return await conversations.create_conversation(input, 'user')

@router.put("/conversations/{conversation_id}/messages", response_model=OutputConversation)
async def add_message(
    conversation_id: str, 
    body: InputMessage,
    conversations: ConversationService = Depends(create_conversation_service)
)->OutputConversation:
    return await conversations.add_messages(conversation_id, [body])

@router.put("/conversations/{conversation_id}/messages/{message_id}/feedback", response_model=OutputConversation)
async def add_feedback(
    conversation_id: str, 
    message_id: int, 
    body: InputFeedback,
    conversations: ConversationService = Depends(create_conversation_service)
)->OutputConversation:
    return await conversations.add_feedback(conversation_id, message_id, body, 'user')

@router.get("/conversations", response_model=List[OutputConversation])
async def list_conversations(
    conversations: ConversationService = Depends(create_conversation_service)
)->OutputConversation:
    return await conversations.find_all({})

@router.get("/conversations/{conversation_id}", response_model=OutputConversation)
async def get_conversation_by_id(
    conversation_id: str, 
    conversations: ConversationService = Depends(create_conversation_service)
)->OutputConversation:
    return await conversations.find_by_id(conversation_id)
