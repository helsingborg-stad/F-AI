from typing import Any, Callable

from langstream import Stream

from fai_backend.assistant.config import provider_map, pipeline_map
from fai_backend.assistant.models import AssistantTemplate, AssistantStreamPipelineDef, \
    AssistantStreamConfig
from fai_backend.assistant.protocol import IAssistantContextStore


class Assistant:
    def __init__(
            self,
            template: AssistantTemplate,
            get_context_store: Callable[[], IAssistantContextStore]
    ):
        self.template = template
        self.get_context_store = get_context_store

    async def create_stream(self) -> Stream[str, str]:
        context_store = self.get_context_store()

        def preprocess(user_query: str):
            context = context_store.get_mutable()
            context.query = user_query
            context.files_collection_id = self.template.files_collection_id
            context.history = []  # TODO
            return user_query

        def update_previous_stream_output(previous_stream_raw_output: Any):
            def parse_in_data(data: Any):
                if isinstance(data, list):
                    return "".join([parse_in_data(c) for c in data])
                return str(data)

            output_as_str = parse_in_data(previous_stream_raw_output)
            context = context_store.get_mutable()
            context.previous_stream_output = output_as_str
            return previous_stream_raw_output

        stream = Stream('preprocess', preprocess)

        for stream_def in self.template.streams:
            new_stream = await self._create_stream_from_config(stream_def, context_store)
            stream = (stream
                      .and_then(update_previous_stream_output)
                      .and_then(new_stream))

        return stream

    @staticmethod
    async def _create_stream_from_config(
            config: AssistantStreamConfig | AssistantStreamPipelineDef,
            context_store: IAssistantContextStore
    ) -> Stream[str, str]:
        if isinstance(config, AssistantStreamConfig):
            llm = provider_map[config.provider](config.settings)
            return await llm.create_llm_stream(config.messages, context_store)

        pipeline = pipeline_map[config.pipeline]()
        return await pipeline.create_pipeline(context_store)
