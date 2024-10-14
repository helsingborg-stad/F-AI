from datetime import datetime

from langstream import Stream

from fai_backend.assistant.config import provider_map, pipeline_map, insert_map
from fai_backend.assistant.helper import messages_expander_stream
from fai_backend.assistant.models import AssistantTemplate, AssistantStreamPipelineDef, \
    AssistantStreamConfig, AssistantStreamMessage
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
        context = self.context_store.get_mutable()
        context.conversation_id = conversation_id
        context.files_collection_id = self.template.files_collection_id
        history_model = await chat_history_repo.get(conversation_id)
        context.history = history_model.history if history_model else []

        def set_query(user_query: str):
            current_context = self.context_store.get_mutable()
            current_context.query = user_query
            return user_query

        async def add_user_query_to_history(in_data: [str]):
            # TODO: Bug: user query is added to history BEFORE template expansion -
            #  causing user query ({query}) to be added twice to LLM input messages...
            user_query = in_data[0]
            await self.context_store.get_mutable().add_to_history(
                [AssistantStreamMessage(
                    timestamp=datetime.now().isoformat(),
                    role='user',
                    content=user_query
                )], chat_history_repo)
            yield user_query

        def postprocess_stream(collected_previous_stream_output: list[str]):
            output_as_str = "".join([s for s in collected_previous_stream_output])
            current_context = self.context_store.get_mutable()
            current_context.previous_stream_output = output_as_str
            return output_as_str

        stream = (Stream('start', set_query)
                  .and_then(add_user_query_to_history))

        for stream_def in self.template.streams:
            new_stream = await self._create_stream_from_config(stream_def, self.context_store)
            stream = (stream
                      .and_then(postprocess_stream)
                      .and_then(new_stream))

        def on_error(e: Exception):
            print(f'assistant stream error: {str(e)}')
            raise e

        return stream.on_error(on_error)

    async def _create_stream_from_config(
            self,
            config: AssistantStreamConfig | AssistantStreamPipelineDef,
            context_store: IAssistantContextStore
    ) -> Stream[list[str], str]:
        if isinstance(config, AssistantStreamConfig):
            if config.provider not in provider_map:
                raise ValueError(f'Unsupported provider "{config.provider}"')

            llm = provider_map[config.provider](config.settings)
            new_stream = await llm.create_llm_stream(config.messages, context_store, self.get_insert)
            return messages_expander_stream(config.messages, context_store, self.get_insert).and_then(new_stream)

        pipeline = pipeline_map[config.pipeline]()
        return await pipeline.create_pipeline(context_store)

    @staticmethod
    def get_insert(name: str) -> IAssistantMessageInsert:
        return insert_map[name]()
