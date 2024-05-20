import asyncio
from random import uniform

from langstream import Stream

from fai_backend.llm.protocol import ILLMStreamProtocol
from fai_backend.llm.models import LLMDataPacket


class ParrotLLM(ILLMStreamProtocol):
    """
    Parrot (mock) LLM protocol reference implementation.

    Parrot will respond with the same message as its input, with a random delay between tokens (words).
    """

    def __init__(self, min_delay: float = 0.1, max_delay: float = 1.0):
        self.min_delay = min_delay
        self.max_delay = max_delay

    async def to_generator(self, input_message: str):
        import re
        parts = re.findall(r'\S+\s*', input_message)
        for part in parts:
            yield part
            await asyncio.sleep(uniform(self.min_delay, self.max_delay))

    async def create(self) -> Stream[str, LLMDataPacket]:
        return Stream[str, str](
            "ParrotStream",
            self.to_generator
        ).map(lambda delta: LLMDataPacket(content=delta, user_friendly=True))
