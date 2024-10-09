import chromadb

from fai_backend.config import settings
from fai_backend.vector.base_chromadb import BaseChromaDB
import chromadb.utils.embedding_functions as default_embedding_function

default_embedding_function = default_embedding_function.OpenAIEmbeddingFunction(
    api_key=settings.OPENAI_API_KEY.get_secret_value(),
    model_name="text-embedding-3-small"
)


class ChromaDB(BaseChromaDB):
    def __init__(self, db_directory: str):
        super().__init__(
            chromadb.PersistentClient(
                path=db_directory,
                settings=chromadb.Settings(
                    anonymized_telemetry=False,  # opt out of telemetry
                    allow_reset=True
                )
            ),
            default_embedding_function=default_embedding_function
        )