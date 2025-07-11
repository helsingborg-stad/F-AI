from typing import AsyncGenerator

from src.modules.llm.models.Delta import Delta
from src.modules.llm.models.Message import Message


async def collect_streamed(generator: AsyncGenerator[Delta, None]):
    role: str | None = None
    content: str | None = None
    reasoning_content: str | None = None

    async for output in generator:
        role = output.role if output.role else role
        content = (content or '') + output.content if output.content else content
        reasoning_content = ((reasoning_content or '') +
                             output.reasoning_content) if output.reasoning_content else reasoning_content

    return Message(
        role=role,
        content=content,
        reasoning_content=reasoning_content,
    )
