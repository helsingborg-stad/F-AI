"""
The factory act as the single entrypoint for interacting with a module's logic.

It produces an instance of a service that can be used to interact further.

If a service has any external dependencies (other modules' protocols/models)
the factory collects them (from __init__) and injects them (through the
service's __init__).
"""
from typing import Literal

from src.modules.hello_world.protocols.IHelloWorldService import IHelloWorldService
from src.modules.hello_world.services.EnglishHelloWorldService import EnglishHelloWorldService
from src.modules.hello_world.services.SwedishHelloWorldService import SwedishHelloWorldService


class HelloWorldFactory:
    def __init__(self, lang: Literal['en', 'sv']):
        self.lang = lang

    async def get(self) -> IHelloWorldService:
        if self.lang == 'en':
            return EnglishHelloWorldService()
        if self.lang == 'sv':
            return SwedishHelloWorldService()
        raise ValueError(f'Unsupported language: {self.lang}')
