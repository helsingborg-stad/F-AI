import json
from typing import Callable, List, Optional, AsyncGenerator, TypeAlias

import openai
from langstream import Stream, StreamOutput
from openai.types.chat import ChatCompletionToolParam
from pydantic import BaseModel

from fai_backend.assistant.helper import get_message_content
from fai_backend.assistant.models import AssistantStreamMessage, ToolCall, ToolCallFunction
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantContextStore, IAssistantMessageInsert
from fai_backend.repositories import chat_history_repo
from fai_backend.utils import get_iso_timestamp_now_utc


# TODO move into part of assistant history (provider agnostic)
class InputMessage(BaseModel):
    role: str
    content: str
    tool_calls: Optional[list[ToolCall]] = None
    tool_call_id: Optional[str] = None


class ResponseDelta(BaseModel):
    """
    Response from LLM, possibly partial in case of content. Tool call is always complete.
    """
    role: str | None
    content: Optional[str]
    tool_calls: list[ToolCall] = []


StreamType: TypeAlias = Stream[str, ResponseDelta]
PipeGeneratorType: TypeAlias = AsyncGenerator[ResponseDelta, None]
EmptyResponseDelta = ResponseDelta(role=None, content="")

# TODO fill with functions from somewhere
function_map = {
    'get_delivery_date': lambda _: "2024-12-30T08:30:00.000Z"
}


class OpenAIStream(StreamType):

    def __init__(
            self,
            name: str,
            call: Callable[
                [str],
                List[InputMessage],
            ],
            model: str,
            url: str = None,
            api_key: str = None,
            temperature: Optional[float] = 0,
            tools: List[ChatCompletionToolParam] = None
    ) -> None:
        self._client = openai.AsyncOpenAI(
            base_url=url,
            api_key=api_key,
        )

        async def chat_completion(
                messages: List[InputMessage],
        ) -> AsyncGenerator[StreamOutput[ResponseDelta], None]:
            try:
                print(f"{len(messages)} messages")
                for m in messages:
                    print(f"\t{m.model_dump(exclude_none=True)}")

                completions = await self._client.chat.completions.create(
                    model=model,
                    messages=[m.model_dump(exclude_none=True) for m in messages],
                    temperature=temperature,
                    stream=True,
                    tools=tools
                )

                pending_function_name: Optional[str] = None
                pending_function_args: Optional[str] = None
                pending_function_call_id: Optional[str] = None

                role: str | None = None

                async for output in completions:
                    if len(output.choices) == 0:
                        continue

                    delta = output.choices[0].delta
                    print(f"resp: {role=} {delta=}")
                    if not delta:
                        continue

                    role = delta.role or role

                    if delta.tool_calls is not None and len(delta.tool_calls) > 0:
                        tool_call = delta.tool_calls[0]

                        func_name = tool_call.function.name
                        func_args = tool_call.function.arguments
                        call_id = tool_call.id
                        pending_function_name = func_name if func_name is not None else pending_function_name
                        pending_function_args = (pending_function_args if pending_function_args else "") + func_args \
                            if func_args is not None else pending_function_args

                        pending_function_call_id = call_id \
                            if call_id is not None \
                            else pending_function_call_id

                    if delta.content is not None:
                        yield self._output_wrap(
                            ResponseDelta(
                                role=role,
                                content=delta.content,
                            )
                        )

                if pending_function_name:
                    print(f"tool_call: id={pending_function_call_id}: {pending_function_name}({pending_function_args})")
                    yield self._output_wrap(
                        ResponseDelta(
                            role="assistant",
                            content="",
                            tool_calls=[ToolCall(
                                id=pending_function_call_id,
                                type="function",
                                function=ToolCallFunction(
                                    name=pending_function_name,
                                    arguments=pending_function_args
                                )
                            )]
                        )
                    )
            except Exception as e:
                print(f'Exception @ chat_completion: {str(e)}')
            finally:
                await self._client.close()

        super().__init__(
            name,
            lambda in_data: chat_completion(call(in_data)),
        )


class OpenAIAssistantLLMProvider(IAssistantLLMProvider):
    class Settings(BaseModel, extra='allow'):
        model: str
        temperature: float = 0

    def __init__(
            self,
            settings: Settings,
            stream_class: type[StreamType] = OpenAIStream
    ):
        self.settings = settings
        self._stream_class = stream_class

    async def create_possibly_recursive_stream(
            self,
            context_store: IAssistantContextStore,
            depth: int
    ) -> Stream[list[str], ResponseDelta]:
        if depth > 5:
            raise Exception("recursive stream depth reached safety limit")

        async def function_handling_pipe(source: PipeGeneratorType):
            new_entry = AssistantStreamMessage(
                timestamp=get_iso_timestamp_now_utc(),
                role="",
                content=""
            )

            context_store.get_mutable().history.append(new_entry)
            index = len(context_store.get_mutable().history) - 1

            async for output in source:
                if len(output.tool_calls) > 0:
                    tool_call = output.tool_calls[0]  # TODO: Handle multiple tool calls?

                    # TODO: Exceptions here are not bubbled up - why ?
                    result = function_map[tool_call.function.name](json.loads(tool_call.function.arguments))

                    print(f"function call result: {tool_call.function.name} result: {json.dumps(result)}")

                    # TODO: Remove when handled by the history pipe
                    tool_call_message = AssistantStreamMessage(
                        timestamp=get_iso_timestamp_now_utc(),
                        role=output.role,
                        content=output.content,
                        tool_calls=output.tool_calls
                    )

                    tool_result_message = AssistantStreamMessage(
                        timestamp=get_iso_timestamp_now_utc(),
                        role="tool",
                        content=json.dumps(result),
                        tool_call_id=tool_call.id
                    )

                    await context_store.get_mutable().add_to_history(
                        [tool_call_message, tool_result_message],
                        chat_history_repo
                    )

                    sub_stream = await self.create_possibly_recursive_stream(
                        context_store,
                        depth=depth + 1
                    )

                    async for sub_output in sub_stream([context_store.get_mutable().history]):  # TODO: weird input?
                        yield sub_output
                else:
                    # TODO: Move to context function "appendToIndex(..)"
                    new_entry.role = output.role
                    new_entry.content += output.content
                    context_store.get_mutable().history[index] = new_entry
                    new_history = await chat_history_repo.get(context_store.get_mutable().conversation_id)
                    new_history.history = context_store.get_mutable().history
                    await chat_history_repo.update(context_store.get_mutable().conversation_id,
                                                   new_history.model_dump(exclude={'id'}, exclude_none=True))
                    yield output

            yield ResponseDelta(role='assistant', content='')

        llm_query_stream: Stream[list[str], ResponseDelta] = self._stream_class(
            "openai",
            lambda in_data: OpenAIAssistantLLMProvider.to_openai_messages(in_data[0], context_store),
            **self.settings.model_dump(),
        )

        return llm_query_stream.pipe(function_handling_pipe)

    async def create_llm_stream(
            self,
            messages: list[AssistantStreamMessage],
            context_store: IAssistantContextStore,
            get_insert: Callable[[str], IAssistantMessageInsert],
    ) -> Stream[list[str], str]:
        stream = await self.create_possibly_recursive_stream(context_store, depth=0)
        return stream.map(lambda delta: delta.content)

    @staticmethod
    def to_openai_message(message: AssistantStreamMessage, context_store: IAssistantContextStore):
        context = context_store.get_mutable()
        return InputMessage(
            role=message.role,
            content=get_message_content(message, context),
            tool_call_id=message.tool_call_id,
            tool_calls=message.tool_calls
        )

    @staticmethod
    def to_openai_messages(in_list: list[AssistantStreamMessage], context_store: IAssistantContextStore):
        if not in_list:
            return []
        converted = [OpenAIAssistantLLMProvider.to_openai_message(m, context_store) for m in in_list if m]
        return converted
