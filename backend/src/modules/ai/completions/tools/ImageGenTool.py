import json

from src.modules.ai.completions.models.ToolCallResult import ToolCallResult
from src.modules.ai.completions.protocols.ITool import ITool
from src.modules.ai.image_gen.factory import ImageGeneratorServiceFactory


class ImageGenTool(ITool):
    def __init__(self, image_generator_factory: ImageGeneratorServiceFactory):
        self.image_generator_factory = image_generator_factory

    def get_tool_definition(self) -> dict:
        return {
            'type': 'function',
            'function': {
                'name': 'generate_image',
                'description': 'Generate an image',
                'strict': True,
                'parameters': {
                    'type': 'object',
                    'properties': {
                        'prompt': {'type': 'string',
                                   'description': 'The prompt to use for the image generation'},
                        'width': {'type': 'integer', 'description': 'The width of the image to generate'},
                        'height': {'type': 'integer', 'description': 'The height of the image to generate'},
                    },
                    'required': ['prompt', 'width', 'height'],
                    'additionalProperties': False,
                }
            }
        }

    async def call_tool(self, args: dict) -> ToolCallResult:
        generator = self.image_generator_factory.get(model='openai/dall-e-3')
        b64 = await generator.generate_by_text(args['prompt'])
        return ToolCallResult(
            result=f'![{args["prompt"][0:15]}](data:image/png;base64,{b64})',
            context_message_override='{"message": "generated an image", "generation_args":' + json.dumps(args) + '}'
        )

    def get_should_feedback_into_llm(self) -> bool:
        return False
