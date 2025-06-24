import os
from collections.abc import AsyncGenerator

from litellm import acompletion

from src.modules.llm.helpers.collect_streamed import collect_streamed
from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message
from src.modules.llm.protocols.ILLMService import ILLMService
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


class LiteLLMService(ILLMService):
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    async def _set_api_keys(self):
        os.environ['OPENAI_API_KEY'] = await self._settings_service.get_setting(SettingKey.OPENAI_API_KEY.key)
        os.environ['MISTRAL_API_KEY'] = await self._settings_service.get_setting(SettingKey.MISTRAL_API_KEY.key)
        os.environ['ANTHROPIC_API_KEY'] = await self._settings_service.get_setting(SettingKey.ANTHROPIC_API_KEY.key)

    async def _clear_api_keys(self):
        os.environ.pop('OPENAI_API_KEY', None)
        os.environ.pop('MISTRAL_API_KEY', None)
        os.environ.pop('ANTHROPIC_API_KEY', None)

    async def stream_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            response_schema: dict[str, object] | None = None,
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> AsyncGenerator[Delta, None]:
        try:
            await self._set_api_keys()
            response = await acompletion(
                model=model.replace(':', '/'),  # patch for old model format
                messages=[
                    {'content': m.content, 'role': m.role} for m in messages if m.content and len(m.content) > 0
                ],
                stream=True,
                api_key=api_key,
            )

            role: str | None = None
            async for output in response:
                if not output or len(output.choices) == 0:
                    continue

                delta = output.choices[0].delta
                role = delta.role or role
                if delta.content is not None:
                    yield Delta(
                        role=role,
                        content=delta.content,
                    )
        finally:
            await self._clear_api_keys()

    async def run_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            response_schema: dict[str, object] | None = None,
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> Message:
        return await collect_streamed(
            stream_llm_func=self.stream_llm,
            model=model,
            api_key=api_key,
            messages=messages,
            response_schema=response_schema,
            extra_params=extra_params
        )
