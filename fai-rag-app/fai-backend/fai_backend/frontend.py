import os
from abc import ABC, abstractmethod

import httpx
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import FileResponse, Response
from starlette.staticfiles import StaticFiles


class FrontendEnvironment(ABC):
    @abstractmethod
    def configure(self, app: FastAPI):
        pass

    @abstractmethod
    async def serve(self, request: Request) -> Response:
        pass


class DevelopmentEnvironment(FrontendEnvironment):
    async def serve(self, request: Request) -> Response:
        async with httpx.AsyncClient() as client:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(f'http://localhost:3000{request.url.path}')
                    return Response(
                        content=resp.content, media_type=resp.headers['Content-Type']
                    )
            except httpx.RequestError:
                raise HTTPException(status_code=404, detail='Item not found')

    def configure(self, app: FastAPI):
        pass


class ProductionEnvironment(FrontendEnvironment):
    def __init__(self, static_dir: str):
        self.static_dir = static_dir

    async def serve(self, request: Request) -> Response:
        return FileResponse(os.path.join(self.static_dir, 'index.html'))

    def configure(self, app: FastAPI):
        app.mount(
            '/assets',
            StaticFiles(directory=os.path.join(self.static_dir, 'assets')),
            name='assets',
        )


def get_frontend_environment(
        env_mode: str, static_dir: str = 'static'
) -> FrontendEnvironment:
    static_dir_path = os.path.join(os.getcwd(), 'fai_backend', static_dir)

    if not os.path.exists(static_dir_path) and env_mode == 'production':
        raise Exception('Static files not found.')

    if not os.path.exists(static_dir_path) and env_mode == 'development':
        return DevelopmentEnvironment()

    return ProductionEnvironment(static_dir_path)
