from typing import Any

from langstream import Stream

from fai_backend.assistant.config import provider_map, pipeline_map, insert_map
from fai_backend.assistant.models import AssistantTemplate, AssistantStreamPipelineDef, \
    AssistantStreamConfig
from fai_backend.assistant.protocol import IAssistantContextStore, IAssistantMessageInsert
from fai_backend.repositories import chat_history_repo


class Assistant:
    def __init__(
            self,
            template: AssistantTemplate,
            context_store: IAssistantContextStore
    ):
        self.template = template
        self.context_store = context_store

    async def create_stream(self, conversation_id: str) -> Stream[str, str]:

        def set_query(user_query: str):
            current_context = self.context_store.get_mutable()
            current_context.query = user_query
            return user_query

        def postprocess_stream(collected_previous_stream_output: list[str]):
            output_as_str = "".join([s for s in collected_previous_stream_output])
            current_context = self.context_store.get_mutable()
            current_context.previous_stream_output = output_as_str
            return output_as_str

        context = self.context_store.get_mutable()
        context.files_collection_id = self.template.files_collection_id
        history_model = await chat_history_repo.get(conversation_id)
        context.history = history_model.history if history_model else []

        stream = Stream('start', set_query)

        for stream_def in self.template.streams:
            new_stream = await self._create_stream_from_config(stream_def, self.context_store)
            stream = (stream
                      .and_then(postprocess_stream)
                      .and_then(new_stream))

        return stream

    async def _create_stream_from_config(
            self,
            config: AssistantStreamConfig | AssistantStreamPipelineDef,
            context_store: IAssistantContextStore
    ) -> Stream[list[str], str]:
        if isinstance(config, AssistantStreamConfig):
            llm = provider_map[config.provider](config.settings)
            return await llm.create_llm_stream(config.messages, context_store, self.get_insert)

        pipeline = pipeline_map[config.pipeline]()
        return await pipeline.create_pipeline(context_store)

    @staticmethod
    def get_insert(name: str) -> IAssistantMessageInsert:
        return insert_map[name]()
