import asyncio
import threading
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter

from src.api.ai import ai_router
from src.api.api_key import api_key_router
from src.api.assistant import assistant_router
from src.api.auth import auth_router
from src.api.chat import chat_router
from src.api.collection import collection_router
from src.api.conversation import conversation_router
from src.api.document_chunker import document_chunker_router
from src.api.group import group_router
from src.api.login import login_router
from src.api.model import model_router
from src.api.settings import settings_router
from src.common.services.create_services import create_services
from src.common.services.models.Services import Services
from src.modules.setup.setup_default_assistants import setup_default_assistants
from src.modules.setup.setup_default_groups import setup_default_groups
from src.modules.setup.setup_default_models import setup_default_models
from src.modules.setup.setup_default_settings import setup_default_settings


async def background_async_worker(services: Services, stop_event: threading.Event):
    while not stop_event.is_set():
        try:
            await services.document_queue_service.run_queue_loop(stop_event)
        except Exception as e:
            print(f"background_async_worker error: {e}")


def background_thread_worker(services: Services, stop_event: threading.Event):
    print("background_thread_worker started")

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(background_async_worker(services, stop_event))
    except Exception as e:
        print(f"background_thread_worker background thread error: {e}")
    finally:
        print("background_thread_worker closing loop")
        loop.close()

    print("background_thread_worker done")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.services = await create_services()
    await setup_default_settings(app.state.services.settings_service)
    await setup_default_groups(app.state.services.group_service)
    await setup_default_models(app.state.services.model_service)
    await setup_default_assistants(app.state.services.assistant_service)

    stop_event = threading.Event()
    background_thread = threading.Thread(
        target=background_thread_worker,
        args=(app.state.services, stop_event),
        daemon=True
    )
    background_thread.start()

    try:
        yield
    finally:
        print("(main) shutting down background thread...")
        stop_event.set()
        background_thread.join(timeout=10)
        if background_thread.is_alive():
            print("(main) background thread did not shut down gracefully")


def create_app():
    load_dotenv()
    new_app = FastAPI(lifespan=lifespan)

    api_router = APIRouter(prefix='/api')

    # Add routes here
    # TODO: move somewhere cooler
    api_router.include_router(api_key_router)
    api_router.include_router(assistant_router)
    api_router.include_router(auth_router)
    api_router.include_router(chat_router)
    api_router.include_router(collection_router)
    api_router.include_router(conversation_router)
    api_router.include_router(document_chunker_router)
    api_router.include_router(group_router)
    api_router.include_router(ai_router)
    api_router.include_router(login_router)
    api_router.include_router(model_router)
    api_router.include_router(settings_router)

    new_app.include_router(api_router)
    return new_app


app_instance = create_app()

if __name__ == '__main__':
    uvicorn.run('main:app_instance', host='0.0.0.0', port=8000, reload=True)
