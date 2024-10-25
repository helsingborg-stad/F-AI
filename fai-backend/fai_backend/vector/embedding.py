from collections.abc import Callable
from typing import Literal

import numpy as np
from chromadb.utils import embedding_functions

from fai_backend.config import settings


class EmbeddingFnFactory:
    @staticmethod
    def create(embedding_model: Literal['default', 'text-embedding-3-small', 'text-embedding-3-large'] | None) -> \
            Callable[[str], np.ndarray]:
        embedding_model_map = {
            'default': embedding_functions.DefaultEmbeddingFunction(),
            'text-embedding-3-small': embedding_functions.OpenAIEmbeddingFunction(
                api_key=settings.OPENAI_API_KEY.get_secret_value(),
                model_name='text-embedding-3-small'
            )
        }

        return embedding_model_map[embedding_model or 'default']
