from typing import Callable, Any, List, Optional, AsyncGenerator, cast, Union, Literal, Awaitable

import openai
from langstream import Stream, StreamOutput
from langstream.contrib import OpenAIChatDelta, OpenAIChatMessage
from pydantic import BaseModel

from fai_backend.assistant.helper import messages_expander_stream, get_message_content
from fai_backend.assistant.models import AssistantStreamMessage, AssistantStreamInsert
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantContextStore, IAssistantMessageInsert


class OpenAIStream(Stream[str, OpenAIChatDelta]):
    def __init__(
            self,
            name: str,
            call: Callable[
                [str],
                List[OpenAIChatMessage],
            ],
            model: str,
            url: str = None,
            api_key: str = None,
            temperature: Optional[float] = 0,
            response_format: Optional[Any] = None
    ) -> None:
        self._client = openai.AsyncOpenAI(
            base_url=url,
            api_key=api_key,
        )

        async def chat_completion(
                messages: List[OpenAIChatMessage],
        ) -> AsyncGenerator[StreamOutput[OpenAIChatDelta], None]:
            try:
                completions = await self._client.chat.completions.create(
                    model=model,
                    messages=[m.to_dict() for m in messages],
                    temperature=temperature,
                    stream=True,
                    response_format=response_format
                )

                async for output in completions:
                    if len(output.choices) == 0:
                        continue

                    delta = output.choices[0].delta
                    if not delta:
                        continue

                    if delta.content is not None:
                        role = cast(
                            Union[Literal["assistant", "function"], None], delta.role
                        )
                        yield self._output_wrap(
                            OpenAIChatDelta(
                                role=role,
                                content=delta.content,
                            )
                        )
            except Exception as e:
                print(f'Exception @ chat_completion: {str(e)}')
                raise e
            finally:
                await self._client.close()

        super().__init__(
            name,
            lambda in_data: chat_completion(call(in_data)),
        )


MessagesProducerType = Callable[[Any], list[OpenAIChatMessage]]
StreamProducerType = Callable[[str, MessagesProducerType, ...], Awaitable[OpenAIStream]]


class OpenAIAssistantLLMProvider(IAssistantLLMProvider):
    class Settings(BaseModel, extra='allow'):
        model: str
        temperature: float = 0

    @staticmethod
    async def _default_openai_stream_constructor(name, messages, model, **kwargs):
        return OpenAIStream(name=name, call=messages, model=model, **kwargs)

    def __init__(
            self,
            settings: Settings,
            stream_producer: StreamProducerType = _default_openai_stream_constructor
    ):
        self.settings = settings
        self._stream_producer = stream_producer

    async def create_llm_stream(
            self,
            messages: list[AssistantStreamMessage | AssistantStreamInsert],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert],
    ) -> Stream[Any, Any]:
        def convert_messages(in_list: list[AssistantStreamMessage]):
            converted = [self._to_openai_message(m, context_store) for m in in_list]
            return converted

        main_stream = (await self._stream_producer(
            "openai",
            lambda in_data: convert_messages(in_data[0]),
            **self.settings.dict(),
        )).map(lambda delta: delta.content)

        return messages_expander_stream(messages, context_store, get_insert).and_then(main_stream)

    @staticmethod
    def _to_openai_message(message: AssistantStreamMessage, context_store: IAssistantContextStore):
        context = context_store.get_mutable()
        return OpenAIChatMessage(
            content=get_message_content(message, context),
            role=message.role
        )

    @staticmethod
    async def _parse_messages(
            messages: list[AssistantStreamMessage | AssistantStreamInsert],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert]
    ):
        context = context_store.get_mutable()

        async def parse_one_message(
                message: AssistantStreamMessage | AssistantStreamInsert
        ) -> list[OpenAIChatMessage]:
            if isinstance(message, AssistantStreamMessage):
                return [OpenAIChatMessage(
                    content=get_message_content(message, context),
                    role=message.role
                )]
            insert_messages = await get_insert(message.insert).get_messages(context_store)
            return [OpenAIChatMessage(role=m.role, content=m.content) for m in insert_messages]

        parsed_message_lists = [await parse_one_message(m) for m in messages]
        return [item for sublist in parsed_message_lists for item in sublist]
