from typing import Dict

from pydantic import BaseModel, RootModel

from fai_backend.assistant.provider.openai import OpenAIAssistantLLMProvider, OpenAIStream
from fai_backend.settings.service import SettingsServiceFactory, SettingKey


class VllmConfig(BaseModel, extra='ignore'):
    url: str
    key: str


VllmConfigRoot = RootModel[Dict[str, VllmConfig]]


class VLLMAssistantLLMProvider(OpenAIAssistantLLMProvider):
    def __init__(self, settings: OpenAIAssistantLLMProvider.Settings):
        async def create_vllm_stream(*args, **kwargs):
            model = kwargs['model']
            settings_service = SettingsServiceFactory().get_service()
            vllm_config = await settings_service.get_value(SettingKey.VLLM_CONFIG)
            parsed = VllmConfigRoot.model_validate_json(vllm_config)

            config = parsed.root[model] if model in parsed.root else None

            if config is None:
                raise ValueError(f"No VLLM config for model '{model}'")

            return OpenAIStream(*args, **kwargs, url=config.url, api_key=config.key)

        super().__init__(settings, stream_producer=create_vllm_stream)
