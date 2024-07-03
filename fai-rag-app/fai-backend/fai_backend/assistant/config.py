from typing import Callable, Any

from fai_backend.assistant.pipeline.rag_scoring import RagScoringPipeline
from fai_backend.assistant.pipeline.test import TestExamplePipeline
from fai_backend.assistant.protocol import IAssistantLLMProvider, IAssistantPipelineStrategy
from fai_backend.assistant.provider.openai import OpenAIAssistantLLMProvider

provider_map: dict[str, Callable[[dict[str, Any]], IAssistantLLMProvider]] = {
    "openai": lambda in_settings: OpenAIAssistantLLMProvider(OpenAIAssistantLLMProvider.Settings(**in_settings))
}

pipeline_map: dict[str, Callable[[], IAssistantPipelineStrategy]] = {
    "test": lambda: TestExamplePipeline(),
    "rag_scoring": lambda: RagScoringPipeline()
}
