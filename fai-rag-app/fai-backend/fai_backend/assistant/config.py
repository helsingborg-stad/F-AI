from typing import Callable, Any

from fai_backend.assistant.insert.history import AssistantHistoryInsert
from fai_backend.assistant.insert.history_summary import AssistantHistorySummaryInsert
from fai_backend.assistant.pipeline.rag_scoring import RagScoringPipeline
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantPipelineStrategy, IAssistantMessageInsert
from fai_backend.assistant.provider.openai import OpenAIAssistantLLMProvider
from fai_backend.assistant.provider.vllm import VLLMAssistantLLMProvider

provider_map: dict[str, Callable[[dict[str, Any]], IAssistantLLMProvider]] = {
    'openai': lambda in_settings: OpenAIAssistantLLMProvider(OpenAIAssistantLLMProvider.Settings(**in_settings)),
    'vllm': lambda in_settings: VLLMAssistantLLMProvider(OpenAIAssistantLLMProvider.Settings(**in_settings))
}

pipeline_map: dict[str, Callable[[], IAssistantPipelineStrategy]] = {
    'rag_scoring': lambda: RagScoringPipeline()
}

insert_map: dict[str, Callable[[], IAssistantMessageInsert]] = {
    'history': lambda: AssistantHistoryInsert(),
    'history_summary': lambda: AssistantHistorySummaryInsert()
}
