from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import Depends, FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette import EventSourceResponse
from starlette.responses import HTMLResponse, RedirectResponse

from fai_backend.auth.router import router as auth_router
from fai_backend.config import settings
from fai_backend.dependencies import get_project_user
from fai_backend.documents.routes import router as documents_router
from fai_backend.llm.service import LLMFactory
from fai_backend.vector.routes import router as vector_router
from fai_backend.framework.frontend import get_frontend_environment
from fai_backend.llm.impl.parrot import ParrotLLM
from fai_backend.llm.models import LLMMessage
from fai_backend.llm.serializer.impl.sse import SSESerializer
from fai_backend.logger.console import console
from fai_backend.middleware import remove_trailing_slash
from fai_backend.phrase import phrase as _, set_language
from fai_backend.projects.router import router as projects_router
from fai_backend.qaf.routes import router as qaf_router
from fai_backend.schema import ProjectUser
from fai_backend.setup import setup_db, setup_project


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

app.middleware('http')(remove_trailing_slash)

# Add Cross Origin Resource Sharing middleware to the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend = get_frontend_environment(settings.ENV_MODE)
frontend.configure(app)


@app.get('/chat-stream')
async def chat_stream(question: str):
    llm = LLMFactory.get()
    serializer = SSESerializer()

    print(f"{llm=}")

    async def generator():
        async for output in llm.run(question):
            if isinstance(output.data, str):
                yield serializer.serialize(LLMMessage(
                    type="message",
                    date=datetime.now(),
                    source="Chat AI",
                    content=output.data
                ))
        yield serializer.serialize(LLMMessage(
            type="message_end",
            date=datetime.now()
        ))

    return EventSourceResponse(generator())


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
