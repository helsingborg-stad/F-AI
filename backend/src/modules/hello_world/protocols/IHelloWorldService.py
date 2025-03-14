from typing import Protocol

from src.modules.hello_world.models.Greeting import Greeting


class IHelloWorldService(Protocol):
    def greet(self) -> Greeting:
        ...
