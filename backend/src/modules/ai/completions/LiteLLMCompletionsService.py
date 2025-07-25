import json
import os
from collections.abc import AsyncGenerator

import litellm
from litellm import acompletion
from litellm.types.llms.openai import OpenAIWebSearchOptions, OpenAIWebSearchUserLocation, \
    OpenAIWebSearchUserLocationApproximate
from litellm.types.utils import ChatCompletionDeltaToolCall

from src.modules.ai.completions.models.Delta import Delta
from src.modules.ai.completions.models.Feature import Feature
from src.modules.ai.completions.models.Message import Message
from src.modules.ai.completions.protocols.ICompletionsService import ICompletionsService
from src.modules.ai.completions.tools.CompletionsToolsFactory import CompletionsToolsFactory
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


class LiteLLMCompletionsService(ICompletionsService):
    def __init__(self, settings_service: ISettingsService, model: str, api_key: str = ''):
        self._settings_service = settings_service
        self._model = model
        self._api_key = api_key

    async def _set_api_keys(self):
        os.environ['OPENAI_API_KEY'] = await self._settings_service.get_setting(SettingKey.OPENAI_API_KEY.key)
        os.environ['MISTRAL_API_KEY'] = await self._settings_service.get_setting(SettingKey.MISTRAL_API_KEY.key)
        os.environ['ANTHROPIC_API_KEY'] = await self._settings_service.get_setting(SettingKey.ANTHROPIC_API_KEY.key)

    async def _clear_api_keys(self):
        os.environ.pop('OPENAI_API_KEY', None)
        os.environ.pop('MISTRAL_API_KEY', None)
        os.environ.pop('ANTHROPIC_API_KEY', None)

    async def run_completions(
            self,
            messages: list[Message],
            enabled_features: list[Feature],
            extra_params: dict | None = None
    ) -> AsyncGenerator[Delta, None]:
        try:
            await self._set_api_keys()
            model = self._model.replace(':', '/')  # patch for old model format

            web_search_requested = Feature.WEB_SEARCH in enabled_features
            web_search_enabled = web_search_requested and litellm.supports_web_search(model)
            web_search_options = OpenAIWebSearchOptions(
                search_context_size='medium',
                user_location=OpenAIWebSearchUserLocation(
                    type='approximate',
                    approximate=OpenAIWebSearchUserLocationApproximate(
                        city='',
                        country='SE',
                        region='',
                        timezone='Europe/Stockholm',
                    )
                )
            )

            if web_search_requested and not web_search_enabled:
                print(f'WARNING: Web search was requested but is not supported by this model ({model}).')

            reasoning_requested = Feature.REASONING in enabled_features
            reasoning_enabled = reasoning_requested and litellm.supports_reasoning(model)

            if reasoning_requested and not reasoning_enabled:
                print(f'WARNING: Reasoning was requested but is not supported by this model ({model}).')

            messages = [
                {'content': m.content, 'role': m.role} for m in messages if m.content and len(m.content) > 0
            ]

            response = await acompletion(
                model=model,
                messages=messages,
                stream=True,
                api_key=self._api_key,
                reasoning_effort="medium" if reasoning_enabled else None,

                # workaround for a bug in tool_call_cost_tracking.py:_get_web_search_options(kwargs) when explicitly setting value to None
                **{'web_search_options': web_search_options} if web_search_enabled else {},

                **(extra_params if extra_params else {})
            )

            role: str | None = None

            async for output in response:
                if not output or len(output.choices) == 0:
                    continue

                delta = output.choices[0].delta
                role = delta.role or role

                if hasattr(delta, 'reasoning_content') and delta.reasoning_content is not None and len(
                        delta.reasoning_content) > 0:
                    yield Delta(
                        role=role,
                        reasoning_content=delta.reasoning_content
                    )

                if delta.content is not None and len(delta.content) > 0:
                    yield Delta(
                        role=role,
                        content=delta.content,
                    )

        finally:
            await self._clear_api_keys()
