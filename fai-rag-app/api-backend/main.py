from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

from src.api.auth import auth_router
from src.api.api_key import api_key_router
from src.api.document_chunker import document_chunker_router
from src.api.llm import llm_router
from src.api.collection import collection_router
from src.common.services.create_services import create_services


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.services = await create_services()
    yield


def create_app():
    load_dotenv()
    new_app = FastAPI(lifespan=lifespan)

    api_router = APIRouter(prefix='/api')

    # Add routes here
    # TODO: move somewhere cooler
    api_router.include_router(api_key_router)
    api_router.include_router(auth_router)
    api_router.include_router(collection_router)
    api_router.include_router(document_chunker_router)
    api_router.include_router(llm_router)

    new_app.include_router(api_router)
    return new_app


app_instance = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app_instance', host='0.0.0.0', port=8000, reload=True)
