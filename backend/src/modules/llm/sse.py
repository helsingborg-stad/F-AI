from sse_starlette import ServerSentEvent, EventSourceResponse

from src.modules.llm.protocols.ILLMService import ILLMService


async def event_source_llm_generator(service: ILLMService):
    async def _generator():
        final_output = ''
        async for delta in await service.stream_llm():
            final_output += delta.content
            yield ServerSentEvent(
                event='',
                data=''
            )

    return EventSourceResponse(_generator())
