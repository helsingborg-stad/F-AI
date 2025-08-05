from typing import Protocol


class IImageGeneratorService(Protocol):
    async def generate_by_text(self, prompt: str) -> str:
        ...

    # async def generate_edit(self, image_src: str, prompt: str) -> str:
    #     ...

    # async def generate_variation(self, image_src: str) -> str:
    #     ...
