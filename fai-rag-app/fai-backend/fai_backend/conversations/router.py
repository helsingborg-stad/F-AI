from typing import List

from fastapi import APIRouter, Depends, Security
from fastui import FastUI, AnyComponent

from fai_backend.conversations.dependencies import (
    add_message_request,
    add_feedback_request,
)
from fai_backend.conversations.schema import (
    ResponseConversation,
    ResponseMessage,
)
from fai_backend.conversations.views import (
    conversations_list_view,
    conversations_create_view,
    handle_create_conversation,
    conversation_view,
)
from fai_backend.dependencies import get_authenticated_user

# from src.logger.route_class import APIRouter as LoggingAPIRouter

router = APIRouter(
    prefix="/api",
    tags=["Conversations"],
    # route_class=LoggingAPIRouter,
)


@router.put(
    "/conversations/{conversation_id}/messages",
    response_model=List[ResponseMessage],
    dependencies=[Security(get_authenticated_user)],
)
async def add_message(
    messages: List[ResponseMessage] = Depends(add_message_request),
) -> List[ResponseMessage]:
    return messages


@router.put(
    "/conversations/{conversation_id}/messages/{message_id}/feedback",
    response_model=ResponseConversation,
    dependencies=[Security(get_authenticated_user)],
)
async def add_feedback(
    conversation: ResponseConversation = Depends(add_feedback_request),
) -> ResponseConversation:
    return conversation


@router.get("/conversations", response_model=FastUI, response_model_exclude_none=True)
async def list_conversations_view(
    view: list[AnyComponent] = Depends(conversations_list_view),
) -> list[AnyComponent]:
    return view


@router.get(
    "/conversations/create", response_model=FastUI, response_model_exclude_none=True
)
async def create_conversation_view(
    view: list[AnyComponent] = Depends(conversations_create_view),
) -> list[AnyComponent]:
    return view


@router.post(
    "/conversations/create", response_model=FastUI, response_model_exclude_none=True
)
async def create_conversation(
    on_create: list[AnyComponent] = Depends(handle_create_conversation),
) -> list[AnyComponent]:
    return on_create


@router.get(
    "/conversations/{conversation_id}",
    response_model=FastUI,
    response_model_exclude_none=True,
)
async def conversation_details_view(
    view: list[AnyComponent] = Depends(conversation_view),
) -> list[AnyComponent]:
    return view
