import asyncio
import datetime

from src.modules.chat.protocols.IChatService import IChatService
from sse_starlette import ServerSentEvent, EventSourceResponse


async def event_source_llm_generator(
        calling_uid: str,
        assistant_or_conversation_id: str,
        start_new_conversation: bool,
        user_message: str,
        chat_service: IChatService
):
    async def sse_generator():
        try:
            if start_new_conversation:
                chat_generator = chat_service.start_new_chat(
                    as_uid=calling_uid,
                    assistant_id=assistant_or_conversation_id,
                    message=user_message
                )
            else:
                chat_generator = chat_service.continue_chat(
                    as_uid=calling_uid,
                    conversation_id=assistant_or_conversation_id,
                    message=user_message
                )

            async for chat_event in chat_generator:
                match chat_event.event:
                    case 'conversation_id':
                        yield ServerSentEvent(
                            event='chat.conversation_id',
                            data=chat_event.conversation_id
                        )
                    case 'message':
                        yield ServerSentEvent(
                            event='chat.message',
                            data={
                                'timestamp': datetime.datetime.utcnow().isoformat(),
                                'source': chat_event.source,
                                'message': chat_event.message
                            }
                        )
                    case _:
                        print(f'unhandled chat event {chat_event.event}')
                        yield ServerSentEvent(
                            event=f'chat.{chat_event.event}',
                            data={
                                'timestamp': datetime.datetime.utcnow().isoformat(),
                                'source': chat_event.source,
                                'message': chat_event.message
                            }
                        )
        except asyncio.CancelledError as e:
            # likely user cancelled generating
            raise e

        finally:
            yield ServerSentEvent(
                event='chat.message_end',
                data={
                    'timestamp': datetime.datetime.utcnow().isoformat()
                }
            )

    return EventSourceResponse(sse_generator())
