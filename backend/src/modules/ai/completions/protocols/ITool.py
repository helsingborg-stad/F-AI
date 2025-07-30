from typing import Protocol

from src.modules.ai.completions.models.ToolCallResult import ToolCallResult


class ITool(Protocol):
    def get_tool_definition(self) -> dict:
        ...

    async def call_tool(self, args: dict) -> ToolCallResult:
        ...

    def get_should_feedback_into_llm(self) -> bool:
        """
        Get if the output of the tool is intended to be fed back into LLM,
        or if it is generally intended to be shown to the end user.
        :return: True if output should be fed back into LLM, False otherwise.
        """
