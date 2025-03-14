import os

from pymongo import AsyncMongoClient

from src.common.services.models.Services import Services
from src.modules.api_key.factory import ApiKeyServiceFactory
from src.modules.auth.authentication.factory import AuthenticationServiceFactory
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType
from src.modules.auth.authorization.factory import AuthorizationServiceFactory
from src.modules.collections.factory import CollectionServiceFactory
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.groups.factory import GroupServiceFactory
from src.modules.llm.factory import LLMServiceFactory
from src.modules.login.factory import LoginServiceFactory
from src.modules.notification.factory import NotificationServiceFactory
from src.modules.settings.factory import SettingsServiceFactory
from src.modules.vector.factory import VectorServiceFactory


async def create_services() -> Services:
    mongo_database = AsyncMongoClient(os.environ['MONGO_URI'])[os.environ['MONGO_DB']]
    api_key_service = ApiKeyServiceFactory(mongo_database).get()
    document_chunker_factory = DocumentChunkerFactory()
    vector_service = VectorServiceFactory().get()
    notification_service = NotificationServiceFactory().get()
    group_service = GroupServiceFactory(mongo_database=mongo_database).get()
    authorization_service = AuthorizationServiceFactory(
        mongo_database=mongo_database,
        api_key_service=api_key_service,
        group_service=group_service,
    ).get()

    return Services(
        authentication_factory=AuthenticationServiceFactory(
            supported_auth_methods=[
                AuthenticationType.GUEST,
                AuthenticationType.API_KEY,
                AuthenticationType.BEARER_TOKEN,
                AuthenticationType.COOKIE_TOKEN
            ],
            api_key_service=api_key_service,
        ),
        authorization_service=authorization_service,
        api_key_service=api_key_service,
        llm_service=LLMServiceFactory().get(),
        document_chunker_factory=document_chunker_factory,
        vector_service=vector_service,
        collection_service=CollectionServiceFactory(
            mongo_database=mongo_database,
            vector_service=vector_service,
            chunker_factory=document_chunker_factory).get(),
        notification_service=notification_service,
        login_service=LoginServiceFactory(
            mongo_database=mongo_database,
            authorization_service=authorization_service,
            notification_service=notification_service
        ).get(),
        group_service=group_service,
        settings_service=SettingsServiceFactory(mongo_database=mongo_database).get(),
    )
