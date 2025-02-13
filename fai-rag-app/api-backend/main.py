from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from src.api.llm import router as llm_router


def create_app():
    load_dotenv()
    new_app = FastAPI()
    api_router = APIRouter(prefix='/api')
    api_router.include_router(llm_router)
    new_app.include_router(api_router)
    return new_app


app = create_app()
