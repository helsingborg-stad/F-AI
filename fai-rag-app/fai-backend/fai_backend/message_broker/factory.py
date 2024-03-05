from typing import TypeVar

from fai_backend.config import settings
from fai_backend.message_broker.interface import IMessageQueue
from fai_backend.message_broker.memory import MemoryQueue

T = TypeVar('T', bound=IMessageQueue)


class MessageBroker:
    _builders = {}

    @classmethod
    def register(cls, broker_type) -> callable:
        def decorator(builder):
            if broker_type in cls._builders:
                raise KeyError(f"A builder for '{broker_type}' is already registered.")
            cls._builders[broker_type] = builder

            return builder

        return decorator

    @classmethod
    def create(cls, broker_type, *args, **kwargs):
        if broker_type not in cls._builders:
            raise KeyError(f"No builder registered for type {broker_type}")
        return cls._builders[broker_type](*args, **kwargs)

    @classmethod
    def list_types(cls) -> dict:
        return cls._builders


# @MessageBroker.register('redis_queue')
# def create_redis_queue(*args, **kwargs) -> IMessageQueue:
#     return RedisQueue(*args, **kwargs)


@MessageBroker.register('memory_queue')
def create_memory_queue() -> IMessageQueue:
    return MemoryQueue()


message_broker = MessageBroker.create(settings.App_MESSAGE_BROKER)
