import os

from pymongo import AsyncMongoClient

from src.common.services.models.Services import Services
from src.modules.ai.completions.tools.CompletionsToolsFactory import CompletionsToolsFactory
from src.modules.ai.image_gen.factory import ImageGeneratorServiceFactory
from src.modules.api_key.factory import ApiKeyServiceFactory
from src.modules.assistants.factory import AssistantServiceFactory
from src.modules.auth.authentication.factory import AuthenticationServiceFactory
from src.modules.auth.authentication.models.AuthenticationType import AuthenticationType
from src.modules.auth.authorization.factory import AuthorizationServiceFactory
from src.modules.chat.factory import ChatServiceFactory, MessageStoreServiceFactory
from src.modules.collections.factory import CollectionServiceFactory
from src.modules.conversations.factory import ConversationServiceFactory
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.groups.factory import GroupServiceFactory
from src.modules.ai.completions.factory import CompletionsServiceFactory
from src.modules.login.factory import LoginServiceFactory
from src.modules.models.factory import ModelServiceFactory
from src.modules.notification.factory import NotificationServiceFactory
from src.modules.resources.factory import ResourceServiceFactory
from src.modules.settings.factory import SettingsServiceFactory
from src.modules.token.factory import TokenServiceFactory
from src.modules.vector.factory import VectorServiceFactory


async def create_services() -> Services:
    mongo_client = AsyncMongoClient(os.environ['MONGO_URI'])
    mongo_database = mongo_client[os.environ['MONGO_DB']]
    api_key_service = ApiKeyServiceFactory(mongo_database).get()
    document_chunker_factory = DocumentChunkerFactory()
    group_service = GroupServiceFactory(mongo_database=mongo_database).get()
    authorization_service = AuthorizationServiceFactory(
        mongo_database=mongo_database,
        api_key_service=api_key_service,
        group_service=group_service,
    ).get()
    settings_service = SettingsServiceFactory(mongo_database=mongo_database).get()
    notification_service = NotificationServiceFactory(settings_service=settings_service).get()
    vector_service = VectorServiceFactory(settings_service=settings_service).get()
    resource_service = ResourceServiceFactory(group_service=group_service).get()
    model_service = ModelServiceFactory(mongo_database=mongo_database).get()
    assistant_service = AssistantServiceFactory(
        mongo_database=mongo_database, 
        resource_service=resource_service,
        model_service=model_service
    ).get()
    conversation_service = ConversationServiceFactory(mongo_database=mongo_database).get()
    image_generator_factory = ImageGeneratorServiceFactory()
    completions_tools_factory = CompletionsToolsFactory(image_generator_factory=image_generator_factory)
    completions_factory = CompletionsServiceFactory(setting_service=settings_service,
                                                    completions_tools_factory=completions_tools_factory)
    collection_service = CollectionServiceFactory(
        mongo_database=mongo_database,
        vector_service=vector_service,
        chunker_factory=document_chunker_factory).get()

    return Services(
        authentication_factory=AuthenticationServiceFactory(
            supported_auth_methods=[
                AuthenticationType.GUEST,
                AuthenticationType.API_KEY,
                AuthenticationType.BEARER_TOKEN,
                AuthenticationType.COOKIE_TOKEN
            ],
            api_key_service=api_key_service,
            settings_service=settings_service,
        ),
        authorization_service=authorization_service,
        api_key_service=api_key_service,
        completions_factory=completions_factory,
        document_chunker_factory=document_chunker_factory,
        vector_service=vector_service,
        collection_service=collection_service,
        notification_service=notification_service,
        login_service=await LoginServiceFactory(
            mongo_database=mongo_database,
            authorization_service=authorization_service,
            notification_service=notification_service,
            settings_service=settings_service,
        ).get(),
        group_service=group_service,
        settings_service=settings_service,
        assistant_service=assistant_service,
        model_service=model_service,
        conversation_service=conversation_service,
        chat_service=ChatServiceFactory(
            completions_factory=completions_factory,
            assistant_service=assistant_service,
            conversation_service=conversation_service,
            collection_service=collection_service,
        ).get(),
        message_store_service=await MessageStoreServiceFactory(mongo_database=mongo_database).get(),
        token_factory=TokenServiceFactory(assistant_service=assistant_service,
                                          conversation_service=conversation_service),
        resource_service=resource_service,
    )
