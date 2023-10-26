from fastapi import APIRouter
from . import conversations

router = APIRouter(prefix="/v1")

router.include_router(conversations.router)
