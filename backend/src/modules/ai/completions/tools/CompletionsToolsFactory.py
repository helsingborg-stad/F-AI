from src.modules.ai.completions.models.Feature import Feature
from src.modules.ai.completions.protocols.ITool import ITool
from src.modules.ai.completions.tools.ImageGenTool import ImageGenTool
from src.modules.ai.image_gen.factory import ImageGeneratorServiceFactory


class CompletionsToolsFactory:
    _tools: dict[str, ITool]

    def __init__(self):
        self._tools = {}

    def get_tools(self, enabled_features: list[Feature]) -> list[dict]:
        tools: list[dict] = []

        return tools

    def _add_tool(self, tool_id: str, tool: ITool):
        tool_def = tool.get_tool_definition()
        self._tools[tool_def['function']['name']] = tool
        self._tools[tool_id] = tool

    def get_tool_by_name(self, function_name: str) -> ITool | None:
        if function_name in self._tools:
            return self._tools[function_name]

        return None
