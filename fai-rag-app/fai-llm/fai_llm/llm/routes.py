from fastapi import APIRouter

from fai_llm.assistant.models import AssistantTemplate, AssistantStreamMessage
from fai_llm.service_locator.service import global_locator

router = APIRouter(
    prefix='/llm',
    tags=['LLM']
)


@router.post('/enqueue', summary='Enqueue an LLM job.')
async def llm_enqueue(
        assistant: AssistantTemplate,
        history: list[AssistantStreamMessage],
        query: str
):
    return {'job_id': 'todo'}


@router.post('/cancel', summary='Cancel a pending LLM job that has not yet been started.')
async def llm_cancel(
        job_id: str
):
    return {'status': 'TODO'}


@router.get('/status', summary='Get LLM job status.')
async def llm_status(
        job_id: str
):
    return {'status': 'TODO'}

# @router.get('/list', summary='List LLM jobs.')
# async def llm_list():
#     return {'status': 'TODO'}
