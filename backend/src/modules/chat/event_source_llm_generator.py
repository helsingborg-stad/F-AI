import asyncio
import json

from sse_starlette import ServerSentEvent, EventSourceResponse

from src.common.get_timestamp import get_timestamp
from src.modules.chat.protocols.IChatService import IChatService
from src.modules.ai.completions.models.Feature import Feature


async def event_source_llm_generator(
        calling_uid: str,
        assistant_or_conversation_id: str,
        start_new_conversation: bool,
        user_message: str,
        chat_service: IChatService,
        features: list[Feature],
        restart_from_id: str | None,
):
    async def sse_generator():
        try:
            if start_new_conversation:
                chat_generator = chat_service.start_new_chat(
                    as_uid=calling_uid,
                    assistant_id=assistant_or_conversation_id,
                    message=user_message,
                    enabled_features=features
                )
            else:
                chat_generator = chat_service.continue_chat(
                    as_uid=calling_uid,
                    conversation_id=assistant_or_conversation_id,
                    message=user_message,
                    enabled_features=features,
                    restart_from_id=restart_from_id
                )

            async for chat_event in chat_generator:
                yield ServerSentEvent(
                    event=f'chat.{chat_event.event}',
                    data=json.dumps({
                        'timestamp': get_timestamp(),
                        **chat_event.model_dump(exclude_none=True)
                    })
                )
        except asyncio.CancelledError as e:
            # likely user cancelled generating
            raise e
        except Exception as e:
            print(f'error generating chat: {e}')
            yield ServerSentEvent(
                event='chat.error',
                data=json.dumps({
                    'timestamp': get_timestamp(),
                    'source': 'error',
                    'message': 'Error:eslg'
                })
            )
            raise e

        finally:
            yield ServerSentEvent(
                event='chat.message_end',
                data=json.dumps({
                    'timestamp': get_timestamp()
                })
            )

    return EventSourceResponse(sse_generator())
