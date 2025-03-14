from src.modules.hello_world.models.Greeting import Greeting
from src.modules.hello_world.protocols.IHelloWorldService import IHelloWorldService


class SwedishHelloWorldService(IHelloWorldService):
    def greet(self) -> Greeting:
        return Greeting(
            language='Swedish',
            text='Hallå världen!'
        )
