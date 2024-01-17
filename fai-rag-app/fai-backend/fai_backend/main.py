from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Form, Request
from starlette.responses import HTMLResponse

from fai_backend.auth.router import router as auth_router
from fai_backend.config import settings
from fai_backend.framework.frontend import get_frontend_environment
from fai_backend.logger.console import console
from fai_backend.middleware import remove_trailing_slash
from fai_backend.projects.router import router as projects_router
from fai_backend.setup import setup_db, setup_project


@asynccontextmanager
async def lifespan(_app: FastAPI):
    console.log('Mounting app')
    await setup_db()
    await setup_project()
    yield
    console.log('Unmounting app')


app = FastAPI(title='FAI RAG App', redirect_slashes=True, lifespan=lifespan)
app.include_router(auth_router)
app.include_router(projects_router)

app.middleware('http')(remove_trailing_slash)

frontend = get_frontend_environment(settings.ENV_MODE)
frontend.configure(app)


@app.get('/health', include_in_schema=False)
async def health_check():
    return {'status': 'healthy'}


@app.get('/api/contact', include_in_schema=True)
async def contact():
    return [
        {
            'type': 'PageWithDrawer',
            'links': [
                {
                    'name': 'Home',
                    'url': '/'
                },
                {
                    'name': 'About',
                    'url': '/about'
                },
                {
                    'name': 'Contact',
                    'url': '/contact'
                },
                {
                    'name': 'Logout',
                    'url': '/logout'
                },
            ],
            'components': [
                {
                    'type': 'Container',
                    'components': [
                        {
                            'type': 'Heading',
                            'level': 1,
                            'text': 'contact'
                        },
                        {
                            'type': 'Paragraph',
                            'level': 1,
                            'text': 'Sint ad duis amet non. Aliqua aliquip nostrud aliquip deserunt eiusmod labore officia.'
                        },
                    ]
                }
            ],
        }
    ]


@app.get('/api/submit-question')
async def submit_question():
    return [
        {
            'type': 'KcForm',
            'action': '/api/submit-question',
            'method': 'POST'
        }
    ]


@app.post('/api/submit-question')
async def submit_question_post(question: Annotated[str, Form()], arrand_id: Annotated[str, Form()]):
    print(question)
    print(arrand_id)


@app.get('/api/about', include_in_schema=True)
async def about():
    return [
        {
            'type': 'PageWithDrawer',
            'links': [
                {
                    'name': 'Home',
                    'url': '/'
                },
                {
                    'name': 'About',
                    'url': '/about'
                },
                {
                    'name': 'Contact',
                    'url': '/contact'
                },
                {
                    'name': 'Logout',
                    'url': '/logout'
                },
            ],
            'components': [
                {
                    'type': 'Container',
                    'components': [
                        {
                            'type': 'Heading',
                            'level': 1,
                            'text': 'about'
                        },
                        {
                            'type': 'Paragraph',
                            'level': 1,
                            'text': 'Sint ad duis amet non. Aliqua aliquip nostrud aliquip deserunt eiusmod labore officia.'
                        },
                    ]
                }
            ],
        }
    ]


@app.get('/api', include_in_schema=True)
async def root():
    return [
        {
            'type': 'PageWithDrawer',
            'links': [
                {
                    'name': 'Home',
                    'url': '/'
                },
                {
                    'name': 'About',
                    'url': '/about'
                },
                {
                    'name': 'Contact',
                    'url': '/contact'
                },
                {
                    'name': 'Logout',
                    'url': '/logout'
                },
            ],
            'components': [
                {
                    'type': 'Container',
                    'components': [
                        {
                            'type': 'Heading',
                            'level': 1,
                            'text': 'Root'
                        },
                        {
                            'type': 'Paragraph',
                            'level': 1,
                            'text': 'Sint ad duis amet non. Aliqua aliquip nostrud aliquip deserunt eiusmod labore officia.'
                        },
                    ]
                }
            ],
        }
    ]


@app.get('/api/{path:path}', status_code=404)
async def set_404():
    return {'404': 'Not Found'}


@app.get('/{path:path}', response_class=HTMLResponse)
async def catch_all(request: Request):
    return await frontend.serve(request)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('fai_backend.main:app', host='0.0.0.0', port=8000, reload=True)
