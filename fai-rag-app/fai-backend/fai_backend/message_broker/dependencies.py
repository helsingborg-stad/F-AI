from fai_backend.config import settings
from fai_backend.message_broker.factory import MessageBroker
from fai_backend.message_broker.interface import IMessageQueue


def get_message_queue() -> IMessageQueue:
    return MessageBroker.create(broker_type=settings.APP_MESSAGE_BROKER_TYPE,
                                host=settings.APP_MESSAGE_BROKER_HOST,
                                port=settings.APP_MESSAGE_BROKER_PORT,
                                password=settings.APP_MESSAGE_BROKER_PASSWORD.get_secret_value() or None,
                                username=settings.APP_MESSAGE_BROKER_USERNAME.get_secret_value() or None)
