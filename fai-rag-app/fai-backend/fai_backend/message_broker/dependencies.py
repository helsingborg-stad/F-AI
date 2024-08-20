from fai_backend.config import settings
from fai_backend.message_broker.factory import MessageBroker
from fai_backend.message_broker.interface import IMessageQueue


def get_message_queue() -> IMessageQueue:
    return MessageBroker.create(settings.APP_MESSAGE_BROKER)