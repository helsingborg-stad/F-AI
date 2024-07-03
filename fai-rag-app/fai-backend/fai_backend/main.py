import uuid
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse, ServerSentEvent
from starlette.responses import HTMLResponse, RedirectResponse

from fai_backend.assistant.assistant import Assistant
from fai_backend.assistant.models import LLMClientChatMessage
from fai_backend.assistant.routes import router as templates_router
from fai_backend.assistant.service import AssistantFactory
from fai_backend.auth.router import router as auth_router
from fai_backend.config import settings
from fai_backend.dependencies import get_project_user
from fai_backend.documents.routes import router as documents_router
from fai_backend.framework.frontend import get_frontend_environment
from fai_backend.logger.console import console
from fai_backend.middleware import remove_trailing_slash
from fai_backend.phrase import phrase as _, set_language
from fai_backend.projects.dependencies import list_projects_request
from fai_backend.projects.router import router as projects_router
from fai_backend.projects.schema import ProjectResponse
from fai_backend.qaf.routes import router as qaf_router
from fai_backend.schema import ProjectUser
from fai_backend.serializer.impl.base64 import Base64Serializer
from fai_backend.setup import setup_db, setup_project
from fai_backend.vector.routes import router as vector_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    console.log('Try setup db')
    await setup_db()
    console.log('Try setup initial project')
    await setup_project()
    yield
    console.log('😴 Unmounting app ...')


app = FastAPI(title='FAI RAG App', redirect_slashes=True, lifespan=lifespan)
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(qaf_router)
app.include_router(documents_router)
app.include_router(vector_router)
app.include_router(templates_router)

app.middleware('http')(remove_trailing_slash)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

frontend = get_frontend_environment(settings.ENV_MODE)
frontend.configure(app)


async def event_source_llm_generator(question: str, assistant: Assistant, conversation_id: str | None):
    serializer = Base64Serializer()

    used_conversation_id = conversation_id or uuid.uuid4().hex

    stream = await assistant.create_stream()

    async def generator(conversation_id_to_send):
        yield ServerSentEvent(
            event="conversation_id",
            data=conversation_id_to_send,
        )

        async for output in stream(question):
            if output.final:
                yield ServerSentEvent(
                    event="message",
                    data=serializer.serialize(LLMClientChatMessage(
                        date=datetime.now(),
                        source="Chat AI",
                        content=output.data
                    )),
                )

        yield ServerSentEvent(
            event="message_end",
            data=serializer.serialize(LLMClientChatMessage(
                date=datetime.now(),
            ))
        )

    return EventSourceResponse(generator(used_conversation_id))


@app.get('/api/assistant-stream/{project}/{assistant}')
async def assistant_stream(
        project: str,
        assistant: str,
        question: str,
        conversation_id: str | None = None,
        projects: list[ProjectResponse] = Depends(list_projects_request)
):
    factory = AssistantFactory([a for p in projects for a in p.assistants if p.id == project])
    assistant_instance = factory.create_assistant(assistant)
    return await event_source_llm_generator(question, assistant_instance, conversation_id)


@app.get('/health', include_in_schema=False)
async def health_check():
    return {'status': 'healthy'}


@app.get('/greet')
async def greet(language: str = Header(default='en')):
    set_language(language)
    return {'message': _('greeting', '')}


@app.get('/api', include_in_schema=True)
async def root(project_user: ProjectUser = Depends(get_project_user)):
    return RedirectResponse(url='/api/questions', status_code=302)


@app.get('/api/{path:path}', status_code=404)
async def set_404():
    return {'404': 'Not Found'}


@app.get('/{path:path}', response_class=HTMLResponse)
async def catch_all(request: Request):
    return await frontend.serve(request)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('fai_backend.main:app', host='0.0.0.0', port=8000, reload=True)
