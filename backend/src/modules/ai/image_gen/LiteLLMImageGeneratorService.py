import litellm

from src.modules.ai.image_gen.protocols.IImageGeneratorService import IImageGeneratorService


class LiteLLMImageGeneratorService(IImageGeneratorService):
    def __init__(self, model: str):
        self._model = model

    async def generate_by_text(self, prompt: str) -> str:
        response = await litellm.aimage_generation(
            model=self._model,
            prompt=prompt,
            response_format="b64_json",
        )
        return response.data[0].b64_json
