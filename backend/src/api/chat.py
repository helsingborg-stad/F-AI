from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.common.services.fastapi_get_services import ServicesDependency
from src.modules.auth.auth_router_decorator import AuthRouterDecorator
from src.modules.auth.authentication.models.AuthenticatedIdentity import AuthenticatedIdentity
from src.modules.chat.event_source_llm_generator import event_source_llm_generator

chat_router = APIRouter(
    prefix='/chat',
    tags=['Chat']
)

auth = AuthRouterDecorator(chat_router)


class CountTokensRequest(BaseModel):
    query: str
    assistant_id: str | None = None
    conversation_id: str | None = None


class CountTokensResponse(BaseModel):
    count: int


@auth.post(
    '/count-tokens',
    ['chat'],
    summary='Count Tokens',
    description='''
Return the (approximate) token count that would be used by
a query to an assistant.

If `conversation_id` is provided the token count will take
into account the history of the conversation.

''',
    response_model=CountTokensResponse,
)
async def count_tokens(body: CountTokensRequest, services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    if body.conversation_id is None and body.assistant_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Must provide assistant_id or conversation_id')

    if body.conversation_id is not None:
        conversation = await services.conversation_service.get_conversation(
            as_uid=auth_identity.uid,
            conversation_id=body.conversation_id
        )

        if conversation is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Conversation not found')

        assistant = await services.assistant_service.get_assistant(
            as_uid=auth_identity.uid,
            assistant_id=conversation.assistant_id
        )

        if assistant is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail='Assistant not found')

        num_tokens = await services.token_factory.get().get_token_count_with_history(
            as_uid=auth_identity.uid,
            conversation_id=body.conversation_id,
            message=body.query)

        return CountTokensResponse(count=num_tokens)

    assistant = await services.assistant_service.get_assistant(
        as_uid=auth_identity.uid,
        assistant_id=body.assistant_id
    )

    if assistant is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Assistant not found')

    num_tokens = await services.token_factory.get().get_token_count(as_uid=auth_identity.uid,
                                                                                   assistant_id=body.assistant_id,
                                                                                   message=body.query)

    return CountTokensResponse(count=num_tokens)


class BufferedChatRequest(BaseModel):
    assistant_id: str
    message: str


class BufferedChatResponse(BaseModel):
    conversation_id: str
    source: str
    message: str


@auth.post(
    '/buffer',
    ['chat'],
    summary='Start new chat (buffered)',
    description='Chat against an assistant. The response is buffered and returned in full once completed.',
    response_model=BufferedChatResponse
)
async def buffered_chat(body: BufferedChatRequest, services: ServicesDependency, auth_identity: AuthenticatedIdentity):
    conversation_id = ''
    final_source = ''
    final_message = ''

    async for delta in services.chat_service.start_new_chat(
            as_uid=auth_identity.uid,
            assistant_id=body.assistant_id,
            message=body.message
    ):
        match delta.event:
            case 'conversation_id':
                conversation_id = delta.conversation_id
            case 'message':
                final_source = delta.source
                final_message += delta.message
            case 'error':
                return BufferedChatResponse(
                    conversation_id="",
                    source="error",
                    message=delta.message
                )
            case _:
                print(f'unhandled chat event {delta.event}')

    return BufferedChatResponse(
        conversation_id=conversation_id,
        source=final_source,
        message=final_message
    )


class BufferedChatContinueRequest(BaseModel):
    message: str


class BufferedChatContinueResponse(BaseModel):
    source: str
    message: str


@auth.post(
    '/buffer/{conversation_id}',
    ['chat'],
    summary='Continue chat (buffered)',
    description='''
Chat against an assistant by continuing an existing conversation. 
The response is buffered and returned in full once completed.
''',
    response_model=BufferedChatContinueResponse
)
async def buffered_chat_continue(
        body: BufferedChatContinueRequest,
        conversation_id: str,
        services: ServicesDependency,
        auth_identity: AuthenticatedIdentity
):
    final_source = ''
    final_message = ''

    async for delta in services.chat_service.continue_chat(
            as_uid=auth_identity.uid,
            conversation_id=conversation_id,
            message=body.message
    ):
        match delta.event:
            case 'message':
                final_source = delta.source
                final_message += delta.message
            case 'error':
                return BufferedChatResponse(
                    conversation_id="",
                    source="error",
                    message=delta.message
                )
            case _:
                print(f'unhandled chat event {delta.event}')

    return BufferedChatContinueResponse(
        source=final_source,
        message=final_message
    )


class StoreMessageRequest(BaseModel):
    message: str


class StoreMessageResponse(BaseModel):
    stored_message_id: str


@auth.post(
    '/store',
    ['chat'],
    summary='Store chat message',
    description='''
Store a chat message to be used with SSE.

This is used as a workaround for submitting long message through
the SSE get request. Stored messages are ephemeral and should be
consumed immediately after calling this endpoint (i.e. by a call 
to `GET /chat/sse` or `GET /chat/sse/{conversation_id}`).
''',
    response_model=StoreMessageResponse
)
async def store_message(body: StoreMessageRequest, services: ServicesDependency):
    stored_message_id = await services.message_store_service.store_message(body.message)

    return StoreMessageResponse(stored_message_id=stored_message_id)


@auth.get(
    '/sse',
    ['chat'],
    summary='Start new chat (streamed via SSE)',
    description='''
Chat against an assistant. 
The response is streamed using Server-Side Events.
    '''
)
async def stream_chat(
        assistant_id: str,
        stored_message_id: str,
        services: ServicesDependency,
        auth_identity: AuthenticatedIdentity
):
    message = await services.message_store_service.consume_message(stored_message_id=stored_message_id)

    if message is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Invalid stored message')

    return await event_source_llm_generator(
        calling_uid=auth_identity.uid,
        assistant_or_conversation_id=assistant_id,
        start_new_conversation=True,
        user_message=message,
        chat_service=services.chat_service,
    )


@auth.get(
    '/sse/{conversation_id}',
    ['chat'],
    summary='Continue chat (streamed via SSE)',
    description='''
Chat against an assistant by continuing an existing conversation.
The response is streamed using Server-Side Events.
    '''
)
async def stream_chat_continue(
        conversation_id: str,
        stored_message_id: str,
        services: ServicesDependency,
        auth_identity: AuthenticatedIdentity
):
    message = await services.message_store_service.consume_message(stored_message_id=stored_message_id)

    if message is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Invalid stored message')

    return await event_source_llm_generator(
        calling_uid=auth_identity.uid,
        assistant_or_conversation_id=conversation_id,
        start_new_conversation=False,
        user_message=message,
        chat_service=services.chat_service,
    )
