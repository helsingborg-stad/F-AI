import asyncio
from typing import Type, TypeVar, Callable

from fai_backend.config import settings
from fai_backend.message_broker.interface import IMessageQueue
from fai_backend.message_broker.memory import MemoryQueue
from fai_backend.message_broker.redis_queue import RedisQueue

T = TypeVar('T', bound=IMessageQueue)


class MessageBroker:
    _builders = {}

    @classmethod
    def register(cls, broker_type) -> Callable:
        def decorator(builder) -> IMessageQueue:
            if broker_type in cls._builders:
                raise KeyError(f"A builder for '{broker_type}' is already registered.")
            cls._builders[broker_type] = builder
            return builder

        return decorator

    @classmethod
    def create(cls, broker_type, *broker_args, **broker_kwargs) -> IMessageQueue:
        if broker_type not in cls._builders:
            raise KeyError(f"No builder registered for type {broker_type}")
        return cls._builders[broker_type](*broker_args, **broker_kwargs)

    @classmethod
    def list_types(cls) -> dict:
        return cls._builders


def create_queue(broker_type: Type[T], *args, **kwargs) -> IMessageQueue:
    return broker_type(*args, **kwargs)


MessageBroker.register('redis_queue')(lambda *args, **kwargs: create_queue(RedisQueue, *args, **kwargs))
MessageBroker.register('memory_queue')(lambda *args, **kwargs: create_queue(MemoryQueue, *args, **kwargs))


if __name__ == '__main__':
    mb = MessageBroker.create(settings.APP_MESSAGE_BROKER)

    for i in range(1, 11):
        job = mb.enqueue('fai_backend.message_broker.tasks.add', i, i, i)

    # async def loop():
    #     while True:
    #         await asyncio.sleep(1)
    #
    #
    # asyncio.run(loop())
