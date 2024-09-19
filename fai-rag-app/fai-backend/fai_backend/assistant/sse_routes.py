from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sse_starlette import ServerSentEvent, EventSourceResponse

from fai_backend.assistant.assistant import Assistant
from fai_backend.assistant.models import LLMClientChatMessage, \
    AssistantStreamMessage, AssistantChatHistoryModel
from fai_backend.assistant.service import AssistantFactory
from fai_backend.dependencies import get_authenticated_user
from fai_backend.projects.dependencies import list_projects_request
from fai_backend.projects.schema import ProjectResponse
from fai_backend.repositories import chat_history_repo
from fai_backend.schema import User
from fai_backend.serializer.impl.base64 import Base64Serializer

sse_router = APIRouter(
    prefix='/api/sse',
    tags=['Assistant'],
)


async def event_source_llm_generator(question: str, assistant: Assistant, conversation_id: str):
    serializer = Base64Serializer()
    stream = await assistant.create_stream(conversation_id)

    async def generator(conversation_id_to_send):
        yield ServerSentEvent(
            event='conversation_id',
            data=conversation_id_to_send,
        )

        start_timestamp = datetime.utcnow().isoformat()

        try:
            history = await chat_history_repo.get(conversation_id_to_send)

            final_output = ''
            async for output in stream(question):
                if output.final:
                    final_output += output.data
                    yield ServerSentEvent(
                        event='message',
                        data=serializer.serialize(LLMClientChatMessage(
                            timestamp=datetime.utcnow().isoformat(),
                            source='Chat AI',
                            content=output.data
                        )),
                    )

            history.history += [
                AssistantStreamMessage(
                    timestamp=start_timestamp,
                    role='user',
                    content=question
                ),
                AssistantStreamMessage(
                    timestamp=datetime.utcnow().isoformat(),
                    role='system',
                    content=final_output
                )
            ]
            await chat_history_repo.update(conversation_id_to_send, history.model_dump(exclude='id'))

        except Exception as e:
            yield ServerSentEvent(
                event='exception',
                data=''
            )
            raise e

        finally:
            yield ServerSentEvent(
                event='message_end',
                data=serializer.serialize(LLMClientChatMessage(
                    timestamp=datetime.utcnow().isoformat(),
                ))
            )

    return EventSourceResponse(generator(conversation_id))


@sse_router.get('/chat/stream/new/{project_id}/{assistant_id}')
async def chat_assistant_stream_new(
        project_id: str,
        assistant_id: str,
        question: str,
        projects: list[ProjectResponse] = Depends(list_projects_request),
        project_user: User = Depends(get_authenticated_user),
):
    factory = AssistantFactory([a for p in projects for a in p.assistants if p.id == project_id])
    assistant_instance = factory.create_assistant(assistant_id)
    new_history_entry = await chat_history_repo.create(AssistantChatHistoryModel(
        user=project_user.email,
        assistant=assistant_instance.template
    ))

    return await event_source_llm_generator(
        question=question,
        assistant=assistant_instance,
        conversation_id=new_history_entry.id
    )


@sse_router.get('/chat/stream/continue/{conversation_id}')
async def chat_assistant_stream_continue(
        conversation_id: str,
        question: str,
        project_user: User = Depends(get_authenticated_user),
):
    chat_history = await chat_history_repo.get(conversation_id)

    if chat_history is None or chat_history.user != project_user.email:
        raise HTTPException(status_code=400)

    assistant_instance = AssistantFactory([]).create_assistant_from_template(chat_history.assistant)

    return await event_source_llm_generator(
        question=question,
        assistant=assistant_instance,
        conversation_id=chat_history.id
    )
