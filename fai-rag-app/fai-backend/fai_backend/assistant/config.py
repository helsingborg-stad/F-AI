from typing import Callable, Any

from fai_backend.assistant.insert.history import AssistantHistoryInsert
from fai_backend.assistant.pipeline.rag_scoring import RagScoringPipeline
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantPipelineStrategy, IAssistantMessageInsert
from fai_backend.assistant.provider.openai import OpenAIAssistantLLMProvider

provider_map: dict[str, Callable[[dict[str, Any]], IAssistantLLMProvider]] = {
    'openai': lambda in_settings: OpenAIAssistantLLMProvider(OpenAIAssistantLLMProvider.Settings(**in_settings))
}

pipeline_map: dict[str, Callable[[], IAssistantPipelineStrategy]] = {
    'rag_scoring': lambda: RagScoringPipeline()
}

insert_map: dict[str, Callable[[], IAssistantMessageInsert]] = {
    'history': lambda: AssistantHistoryInsert()
}
