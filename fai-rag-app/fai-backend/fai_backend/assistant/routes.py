from fastapi import APIRouter
from fai_backend.logger.route_class import APIRouter as LoggingAPIRouter

router = APIRouter(
    prefix='/api',
    tags=['Assistant'],
    route_class=LoggingAPIRouter,
    dependencies=[],
)


@router.get(
    '/assistant/{project_id}')
async def get_assistant(project_id: str):
    return [project_id]


@router.post(
    '/assistant')
async def get_assistant():
    return []
