import asyncio
import json

import openai
from typing import TypeVar, Callable, List, Optional, Dict, Any, Union, Literal, AsyncGenerator, cast

from langstream import Stream, StreamOutput
from langstream.contrib import OpenAIChatDelta, OpenAIChatMessage
from pydantic import BaseModel, RootModel
from retry import retry

from fai_backend.assistant.provider.openai import OpenAIAssistantLLMProvider
from fai_backend.config import settings as fai_backend_settings

T = TypeVar("T")
U = TypeVar("U")


class VllmConfig(BaseModel, extra='ignore'):
    url: str
    key: str


VllmConfigRoot = RootModel[Dict[str, VllmConfig]]


class VLLMStream(Stream[T, U]):
    """
    NOTE: this is a copy-paste of `OpenAIChatStream` except the OpenAI client is overridden with custom settings.
    """

    def __init__(
            self,
            name: str,
            call: Callable[
                [T],
                List[OpenAIChatMessage],
            ],
            model: str,
            vllm_url: str,
            vllm_api_key: str,
            functions: Optional[List[Dict[str, Any]]] = None,
            function_call: Optional[Union[Literal["none", "auto"], Dict[str, Any]]] = None,
            temperature: Optional[float] = 0,
            max_tokens: Optional[int] = None,
            timeout: int = 600,  # TODO: vLLM cold boot could take a LONG time - workaround?
            retries: int = 3,
    ) -> None:
        self._client = openai.OpenAI(
            base_url=vllm_url,
            api_key=vllm_api_key,
        )

        async def chat_completion(
                messages: List[OpenAIChatMessage],
        ) -> AsyncGenerator[StreamOutput[OpenAIChatDelta], None]:
            loop = asyncio.get_event_loop()

            @retry(tries=retries)
            def get_completions():
                function_kwargs = {}
                if functions is not None:
                    function_kwargs["functions"] = functions
                if function_call is not None:
                    function_kwargs["function_call"] = function_call

                return self._client.chat.completions.create(
                    timeout=timeout,
                    model=model,
                    messages=cast(Any, [m.to_dict() for m in messages]),
                    temperature=temperature,
                    stream=True,
                    max_tokens=max_tokens,
                    **function_kwargs,
                )

            completions = await loop.run_in_executor(None, get_completions)

            pending_function_call: Optional[OpenAIChatDelta] = None

            for output in completions:
                if len(output.choices) == 0:
                    continue

                delta = output.choices[0].delta
                if not delta:
                    continue

                if delta.function_call is not None:
                    role = delta.role
                    function_name: Optional[str] = delta.function_call.name
                    function_arguments: Optional[str] = delta.function_call.arguments

                    if function_name is not None:
                        pending_function_call = OpenAIChatDelta(
                            role="function",
                            name=function_name,
                            content=function_arguments or "",
                        )
                    elif (
                            pending_function_call is not None
                            and function_arguments is not None
                    ):
                        pending_function_call.content += function_arguments
                elif delta.content is not None:
                    role = cast(
                        Union[Literal["assistant", "function"], None], delta.role
                    )
                    yield self._output_wrap(
                        OpenAIChatDelta(
                            role=role,
                            content=delta.content,
                        )
                    )
                else:
                    if pending_function_call:
                        yield self._output_wrap(pending_function_call)
                        pending_function_call = None
            if pending_function_call:
                yield self._output_wrap(pending_function_call)
                pending_function_call = None

        super().__init__(
            name,
            lambda input: cast(AsyncGenerator[U, None], chat_completion(call(input))),
        )


class VLLMAssistantLLMProvider(OpenAIAssistantLLMProvider):
    def __init__(self, settings: OpenAIAssistantLLMProvider.Settings):
        def config_injected_vllmstream_constructor(*args, **kwargs):
            model = kwargs['model']
            parsed = VllmConfigRoot.model_validate_json(fai_backend_settings.VLLM_CONFIG)

            config = parsed.root[model] if model in parsed.root else None

            if config is None:
                raise ValueError(f"No VLLM config for model '{model}'")

            return VLLMStream(*args, **kwargs, vllm_url=config.url, vllm_api_key=config.key)

        super().__init__(settings, stream_class=config_injected_vllmstream_constructor)
