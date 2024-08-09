from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from config.service import settings
from fai_llm.app_life.service import AppLifeService
from fai_llm.log.service import MPLogging
from fai_llm.service_locator.service import global_locator
from fai_llm.worker.factory import DefaultWorkerFactory
from ws.routes import router as ws_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global_locator.services.main_logger = MPLogging.get_logger('main')
    global_locator.services.app_life = AppLifeService()
    global_locator.services.worker_service = DefaultWorkerFactory().create()

    global_locator.services.main_logger.info('initialization complete')
    yield
    global_locator.services.app_life.shutdown()
    global_locator.services.main_logger.info('shutdown complete')


app = FastAPI(
    title='FAI LLM Worker',
    lifespan=lifespan
)

app.include_router(ws_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host=settings.LISTEN_ADDRESS, port=settings.LISTEN_PORT, reload=True)
