from fastapi import FastAPI

from backend.server.db.mongodb_conversation import init_db_on_start

from .api.v1.router import router


app = FastAPI(dependencies=[])

init_db_on_start(app)
app.include_router(router, prefix="/api")

