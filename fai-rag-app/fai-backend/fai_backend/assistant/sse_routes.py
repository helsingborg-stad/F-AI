import asyncio
import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sse_starlette import ServerSentEvent, EventSourceResponse

from fai_backend.assistant.assistant import Assistant
from fai_backend.assistant.models import LLMClientChatMessage, AssistantChatHistoryModel, StoredQuestionModel
from fai_backend.assistant.service import AssistantFactory
from fai_backend.dependencies import get_authenticated_user
from fai_backend.projects.dependencies import list_projects_request
from fai_backend.projects.schema import ProjectResponse
from fai_backend.repositories import chat_history_repo, stored_questions_repo
from fai_backend.schema import User
from fai_backend.serializer.impl.base64 import Base64Serializer
from fai_backend.utils import get_iso_timestamp_now_utc

sse_router = APIRouter(
    prefix='/api/sse',
    tags=['Assistant'],
)


async def event_source_llm_generator(question: str, assistant: Assistant, conversation_id: str):
    serializer = Base64Serializer()
    stream = await assistant.create_stream(conversation_id)

    # TODO: Rollback to original history on errors
    async def generator(conversation_id_to_send):
        yield ServerSentEvent(
            event='conversation_id',
            data=conversation_id_to_send,
        )

        try:
            final_output = ''
            async for output in stream(question):
                if output.final:
                    final_output += output.data
                    yield ServerSentEvent(
                        event='message',
                        data=serializer.serialize(LLMClientChatMessage(
                            timestamp=get_iso_timestamp_now_utc(),
                            source='Chat AI',
                            content=output.data
                        )),
                    )

            if final_output == '':
                # Empty LLM response is always an error?
                raise Exception('LLM output is empty')

        except asyncio.CancelledError as e:
            logging.info(f'client disconnected: {str(e)}')
            raise e

        except Exception as e:
            logging.exception(e)
            yield ServerSentEvent(
                event='exception',
                data=''
            )
            raise e

        finally:
            yield ServerSentEvent(
                event='message_end',
                data=serializer.serialize(LLMClientChatMessage(
                    timestamp=get_iso_timestamp_now_utc(),
                ))
            )

    return EventSourceResponse(generator(conversation_id))


class StoreQuestionModel(BaseModel):
    question: str


@sse_router.post('/chat/question')
async def store_question(
        req: StoreQuestionModel,
        project_user: User = Depends(get_authenticated_user)
):
    stored_question: StoredQuestionModel = await stored_questions_repo.create(StoredQuestionModel(
        question=req.question,
        user=project_user.email
    ))

    return {'id': str(stored_question.id)}


@sse_router.get('/chat/stream/new/{project_id}/{assistant_id}')
async def chat_assistant_stream_new(
        project_id: str,
        assistant_id: str,
        stored_question_id: str,
        projects: list[ProjectResponse] = Depends(list_projects_request),
        project_user: User = Depends(get_authenticated_user),
):
    stored = await stored_questions_repo.get(stored_question_id)

    if stored is None:
        raise HTTPException(status_code=404)
    if stored.user != project_user.email:
        raise HTTPException(status_code=403)

    await stored_questions_repo.delete(stored_question_id)

    question = stored.question

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
        stored_question_id: str,
        project_user: User = Depends(get_authenticated_user),
):
    stored = await stored_questions_repo.get(stored_question_id)

    if stored is None:
        raise HTTPException(status_code=404)
    if stored.user != project_user.email:
        raise HTTPException(status_code=403)

    await stored_questions_repo.delete(stored_question_id)

    question = stored.question

    chat_history = await chat_history_repo.get(conversation_id)

    if chat_history is None or chat_history.user != project_user.email:
        raise HTTPException(status_code=400)

    assistant_instance = AssistantFactory([]).create_assistant_from_template(chat_history.assistant)

    return await event_source_llm_generator(
        question=question,
        assistant=assistant_instance,
        conversation_id=chat_history.id
    )
