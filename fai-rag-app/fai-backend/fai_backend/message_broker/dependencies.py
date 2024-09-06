from pydantic import SecretStr

from fai_backend.config import settings
from fai_backend.message_broker.factory import MessageBroker
from fai_backend.message_broker.interface import IMessageQueue


def get_message_queue() -> IMessageQueue:
    def _get_secret_value(prop: SecretStr | str | None) -> str | None:
        return prop.get_secret_value() if isinstance(prop, SecretStr) else None

    return MessageBroker.create(broker_type=settings.MESSAGE_BROKER_TYPE,
                                host=settings.MESSAGE_BROKER_HOST,
                                port=settings.MESSAGE_BROKER_PORT,
                                password=_get_secret_value(settings.MESSAGE_BROKER_PASSWORD),
                                username=_get_secret_value(settings.MESSAGE_BROKER_USERNAME))
