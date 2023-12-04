from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from backend.server.db.mongodb_conversation import init_db_on_start
from .api.v1.router import router

app = FastAPI(dependencies=[])


@app.on_event("startup")
def configure_open_api():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="F-AI Backend",
        version="0.2.0",
        routes=app.routes,
    )
    openapi_schema["openapi"] = "3.0.3"  # specify your version here
    app.openapi_schema = openapi_schema
    return app.openapi_schema


init_db_on_start(app)
app.include_router(router, prefix="/api")
