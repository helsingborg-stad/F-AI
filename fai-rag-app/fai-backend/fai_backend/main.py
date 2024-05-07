from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, Request
from starlette.responses import HTMLResponse, RedirectResponse

from fai_backend.auth.router import router as auth_router
from fai_backend.config import settings
from fai_backend.dependencies import get_project_user
from fai_backend.documents.routes import router as documents_router
from fai_backend.vector.routes import router as vector_router
from fai_backend.framework.frontend import get_frontend_environment
from fai_backend.logger.console import console
from fai_backend.middleware import remove_trailing_slash
from fai_backend.phrase import phrase as _
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

frontend = get_frontend_environment(settings.ENV_MODE)
frontend.configure(app)


@app.get('/health', include_in_schema=False)
async def health_check():
    return {'status': 'healthy'}


@app.get('/greet')
async def greet(language: str = Header(default='en')):
    return {'message': _(key='some_complex_id', default='Hello {first_name}, your last name is {last_name}',
                         first_name='Tim', last_name='Kook')}


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
