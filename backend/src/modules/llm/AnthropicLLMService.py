from collections.abc import AsyncGenerator
from typing import Literal

import anthropic
from anthropic import NOT_GIVEN
from anthropic.types import MessageParam

from src.modules.llm.helpers.collect_streamed import collect_streamed
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message
from src.modules.llm.protocols.ILLMService import ILLMService
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


class AnthropicLLMService(ILLMService):
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    @staticmethod
    def _to_role(role: str) -> Literal['user', 'assistant']:
        role_map: dict[str, Literal['user', 'assistant']] = {
            'user': 'user',
            'assistant': 'assistant',
            'system': 'assistant',
        }
        return role_map.get(role, 'user')

    async def stream_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> AsyncGenerator[Delta, None]:
        [_, model_name] = parse_model_key(model)

        if not api_key or len(api_key) == 0:
            api_key = await self._settings_service.get_setting(SettingKey.ANTHROPIC_API_KEY.key)

        client = anthropic.AsyncAnthropic(api_key=api_key)

        if not extra_params:
            extra_params = {}

        async with client.messages.stream(
                max_tokens=extra_params.get('max_tokens', 16000),
                model=model_name,
                system=next((m.content for m in messages if m.role == 'system'), NOT_GIVEN),
                messages=[
                    MessageParam(
                        role=self._to_role(m.role),
                        content=m.content,
                    )
                    for m in messages if m.role != 'system'
                ]
        ) as stream:
            async for text in stream.text_stream:
                yield Delta(
                    role='assistant',
                    content=text,
                )

    async def run_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> Message:
        return await collect_streamed(
            stream_llm_func=self.stream_llm,
            model=model,
            api_key=api_key,
            messages=messages,
            extra_params=extra_params
        )
