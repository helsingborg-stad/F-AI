from collections.abc import Callable
from typing import Literal

import numpy as np
from chromadb.utils import embedding_functions

from fai_backend.settings.service import SettingsServiceFactory, SettingKey


class EmbeddingFnFactory:
    @staticmethod
    async def create(
            embedding_model: Literal['default', 'text-embedding-3-small', 'text-embedding-3-large'] | None
    ) -> Callable[[str], np.ndarray]:
        settings_service = SettingsServiceFactory().get_service()
        embedding_model_map = {
            'default': embedding_functions.DefaultEmbeddingFunction(),
            'text-embedding-3-small': embedding_functions.OpenAIEmbeddingFunction(
                api_key=await settings_service.get_value(SettingKey.OPENAI_API_KEY),
                model_name='text-embedding-3-small'
            )
        }

        return embedding_model_map[embedding_model or 'default']
