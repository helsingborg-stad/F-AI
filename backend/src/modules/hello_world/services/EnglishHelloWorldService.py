from src.modules.hello_world.models.Greeting import Greeting
from src.modules.hello_world.protocols.IHelloWorldService import IHelloWorldService


class EnglishHelloWorldService(IHelloWorldService):
    def greet(self) -> Greeting:
        return Greeting(
            language='English',
            text='Hello world!'
        )
