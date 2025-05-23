from collections.abc import AsyncGenerator

from mistralai import Mistral, UserMessage, SystemMessage, AssistantMessage

from src.modules.llm.helpers.collect_streamed import collect_streamed
from src.modules.llm.helpers.parse_model_key import parse_model_key
from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message
from src.modules.llm.protocols.ILLMService import ILLMService
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.settings.settings import SettingKey


class MistralLLMService(ILLMService):
    def __init__(self, settings_service: ISettingsService):
        self._settings_service = settings_service

    @staticmethod
    def _to_mistral_message(message: Message):
        match message.role:
            case 'system':
                return SystemMessage(content=message.content)
            case 'assistant':
                return AssistantMessage(content=message.content)
            case 'user':
                return UserMessage(content=message.content)
            case _:
                print(f'(Mistral) unknown role: {message.role}')
                return UserMessage(content=message.content)

    async def stream_llm(
            self,
            model: str,
            api_key: str,
            messages: list[Message],
            response_schema: dict[str, object] | None = None,
            extra_params: dict[str, float | int | bool | str] | None = None
    ) -> AsyncGenerator[Delta, None]:
        [_, model_name] = parse_model_key(model_key=model)

        if not api_key or len(api_key) == 0:
            api_key = await self._settings_service.get_setting(SettingKey.MISTRAL_API_KEY.key)

        client = Mistral(api_key=api_key)

        role: str | None = None

        async for delta in await client.chat.stream_async(
                model=model_name,
                messages=[self._to_mistral_message(m) for m in messages],
        ):
            if len(delta.data.choices) == 0:
                continue

            content_delta = delta.data.choices[0].delta
            role = content_delta.role or role

            if content_delta.content is not None:
                yield Delta(
                    role=role,
                    content=content_delta.content,
                )

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
