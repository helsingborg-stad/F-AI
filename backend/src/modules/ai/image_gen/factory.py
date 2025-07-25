from src.modules.ai.image_gen.LiteLLMImageGeneratorService import LiteLLMImageGeneratorService
from src.modules.ai.image_gen.protocols.IImageGeneratorService import IImageGeneratorService


class ImageGeneratorServiceFactory:
    def __init__(self):
        pass

    def get(self, model: str) -> IImageGeneratorService:
        return LiteLLMImageGeneratorService(model=model)
