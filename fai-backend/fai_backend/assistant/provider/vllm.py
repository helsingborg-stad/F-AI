from typing import TypeVar, Dict

from pydantic import BaseModel, RootModel

from fai_backend.assistant.provider.openai import OpenAIAssistantLLMProvider, OpenAIStream
from fai_backend.config import settings as fai_backend_settings

T = TypeVar("T")
U = TypeVar("U")


class VllmConfig(BaseModel, extra='ignore'):
    url: str
    key: str


VllmConfigRoot = RootModel[Dict[str, VllmConfig]]


class VLLMAssistantLLMProvider(OpenAIAssistantLLMProvider):
    def __init__(self, settings: OpenAIAssistantLLMProvider.Settings):
        def config_injected_vllmstream_constructor(*args, **kwargs):
            model = kwargs['model']
            parsed = VllmConfigRoot.model_validate_json(fai_backend_settings.VLLM_CONFIG)

            config = parsed.root[model] if model in parsed.root else None

            if config is None:
                raise ValueError(f"No VLLM config for model '{model}'")

            return OpenAIStream(*args, **kwargs, url=config.url, api_key=config.key)

        super().__init__(settings, stream_class=config_injected_vllmstream_constructor)
