import collections
from typing import Iterable, Any

import openai
from openai import BadRequestError
from openai.types.chat import ChatCompletionToolParam

from .models.Message import Message
from .models.Delta import Delta
from .models.ToolCall import ToolCall
from .models.ToolCallFunction import ToolCallFunction


class OpenAIRunner:
    def __init__(
            self,
            model: str,
            messages: list[Message],
            max_tokens: int,
            temperature: float,
            url: str | None = None,
            api_key: str | None = None,
            tools: Iterable[ChatCompletionToolParam] = None,
            response_format: Any = None
    ):
        self.model = model
        self.messages = messages
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.url = url
        self.api_key = api_key
        self.tools = tools
        self.response_format = response_format

    async def run(self, message: Message | None = None) -> collections.abc.AsyncGenerator[Delta, None]:
        client = openai.AsyncOpenAI(
            base_url=self.url,
            api_key=self.api_key
        )

        full_messages = self.messages + [message] if message is not None else self.messages

        try:
            stream = await client.chat.completions.create(
                stream=True,
                model=self.model,
                messages=[m.model_dump(exclude_none=True) for m in full_messages],
                temperature=self.temperature,
                max_completion_tokens=self.max_tokens,
                tools=self.tools,
                response_format=self.response_format
            )
        except BadRequestError as e:
            yield Delta(
                role='error',
                content=e.body['message'] if isinstance(e.body, dict) and 'message' in e.body else e.message
            )
            return

        pending_fn_name: str | None = None
        pending_fn_args: str | None = None
        pending_fn_call_id: str | None = None
        role: str | None = None

        async for output in stream:
            if len(output.choices) == 0:
                continue

            # TODO: propagate output.choices[0].finish_reason == 'length' to report max_token limit

            delta = output.choices[0].delta
            if not delta:
                continue

            role = delta.role or role

            if delta.tool_calls is not None and len(delta.tool_calls) > 0:
                tool_call = delta.tool_calls[0]

                fn_name = tool_call.function.name
                fn_args = tool_call.function.arguments
                fn_call_id = tool_call.id
                pending_fn_name = fn_name if fn_name is not None else pending_fn_name
                pending_fn_args = (pending_fn_args if pending_fn_args else "") + fn_args \
                    if fn_args is not None else pending_fn_args

                pending_fn_call_id = fn_call_id \
                    if fn_call_id is not None \
                    else pending_fn_call_id

            if delta.content is not None:
                yield Delta(
                    role=role,
                    content=delta.content,
                )

        if pending_fn_name:
            yield Delta(
                role='assistant',
                tool_calls=[ToolCall(
                    id=pending_fn_call_id,
                    type='function',
                    function=ToolCallFunction(
                        name=pending_fn_name,
                        arguments=pending_fn_args,
                    )
                )]
            )
