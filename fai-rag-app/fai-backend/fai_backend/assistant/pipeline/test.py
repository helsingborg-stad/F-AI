from langstream import Stream

from fai_backend.assistant.models import AssistantStreamMessage
from fai_backend.assistant.protocol import IAssistantPipelineStrategy, IAssistantContextStore
from fai_backend.assistant.provider.openai import OpenAIAssistantLLMProvider


class TestExamplePipeline(IAssistantPipelineStrategy):
    async def create_pipeline(
            self,
            context_store: IAssistantContextStore
    ) -> Stream[str, str]:
        m = [
            AssistantStreamMessage(role="system", content="Rephrase this question in a fancier way"),
            AssistantStreamMessage(role="user", content="{query}")
        ]
        stream = await OpenAIAssistantLLMProvider(OpenAIAssistantLLMProvider.Settings(
            model="gpt-3.5-turbo"
        )).create_llm_stream(m, context_store)
        return stream
