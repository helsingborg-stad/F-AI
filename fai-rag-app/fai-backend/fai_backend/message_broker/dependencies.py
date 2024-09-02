from fai_backend.config import settings
from fai_backend.message_broker.factory import MessageBroker
from fai_backend.message_broker.interface import IMessageQueue


def get_message_queue() -> IMessageQueue:
    return MessageBroker.create(broker_type=settings.APP_MESSAGE_BROKER_TYPE,
                                redis_host=settings.APP_MESSAGE_BROKER_HOST,
                                redis_port=settings.APP_MESSAGE_BROKER_PORT,
                                redis_password=settings.APP_MESSAGE_BROKER_PASSWORD,
                                redis_username=settings.APP_MESSAGE_BROKER_USERNAME,)
