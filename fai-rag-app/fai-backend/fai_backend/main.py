from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk import Hub
from starlette.responses import HTMLResponse, RedirectResponse

from fai_backend.assistant.routes import router as assistant_router
from fai_backend.assistant.sse_routes import sse_router as assistant_sse_router
from fai_backend.auth.router import router as auth_router
from fai_backend.auth.security import authenticate
from fai_backend.config import settings
from fai_backend.dependencies import get_project_user
from fai_backend.documents.routes import router as documents_router
from fai_backend.framework.frontend import get_frontend_environment
from fai_backend.logger.console import console
from fai_backend.middleware import remove_trailing_slash, add_git_revision_to_request_header
from fai_backend.phrase import phrase as _
from fai_backend.phrase import set_language
from fai_backend.projects.router import router as projects_router
from fai_backend.qaf.routes import router as qaf_router
from fai_backend.schema import ProjectUser
from fai_backend.setup import setup_db, setup_project, setup_sentry, setup_file_parser
from fai_backend.vector.routes import router as vector_router
from fai_backend.new_chat.routes import router as new_chat_router
from fai_backend.feedback.routes import router as feedback_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    console.log('Try setup Sentry')
    await setup_sentry()
    console.log('Try setup db')
    await setup_db()
    console.log('Try setup initial project')
    await setup_project()
    console.log('Try setup file parser environment')
    await setup_file_parser()
    yield
    console.log('😴 Unmounting app ...')
    console.log('Shutting down Sentry')
    client = Hub.current.client
    if client is not None:
        client.close(timeout=2.0)


app = FastAPI(title='FAI RAG App', redirect_slashes=True, lifespan=lifespan)
app.include_router(assistant_sse_router)
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(feedback_router)
app.include_router(qaf_router)
app.include_router(new_chat_router)
app.include_router(documents_router)
app.include_router(vector_router)
app.include_router(assistant_router)


app.middleware('http')(add_git_revision_to_request_header)
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


@app.get('/health', include_in_schema=False)
async def health_check():
    return {'status': 'healthy'}


@app.get('/greet', dependencies=[Depends(authenticate)])
async def greet(language: str = Header(default='en')):
    set_language(language)
    return {'message': _('greeting', '')}


@app.get('/api', include_in_schema=True)
async def root(project_user: ProjectUser = Depends(get_project_user)):
    return RedirectResponse(url='/api/chat', status_code=302)


@app.get('/api/{path:path}', status_code=404)
async def set_404():
    return {'404': 'Not Found'}


@app.get('/{path:path}', response_class=HTMLResponse)
async def catch_all(request: Request):
    return await frontend.serve(request)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('fai_backend.main:app', host='0.0.0.0', port=8000, reload=True)
