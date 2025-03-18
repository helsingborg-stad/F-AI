from dataclasses import dataclass

from src.modules.api_key.protocols.IApiKeyService import IApiKeyService
from src.modules.assistants.protocols.IAssistantService import IAssistantService
from src.modules.auth.authentication.factory import AuthenticationServiceFactory
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService
from src.modules.collections.protocols.ICollectionService import ICollectionService
from src.modules.document_chunker.factory import DocumentChunkerFactory
from src.modules.groups.protocols.IGroupService import IGroupService
from src.modules.llm.protocols.ILLMService import ILLMService
from src.modules.login.protocols.ILoginService import ILoginService
from src.modules.notification.protocols.INotificationService import INotificationService
from src.modules.settings.protocols.ISettingsService import ISettingsService
from src.modules.vector.protocols.IVectorService import IVectorService


@dataclass
class Services:
    authentication_factory: AuthenticationServiceFactory
    authorization_service: IAuthorizationService
    api_key_service: IApiKeyService
    llm_service: ILLMService
    document_chunker_factory: DocumentChunkerFactory
    vector_service: IVectorService
    collection_service: ICollectionService
    notification_service: INotificationService
    login_service: ILoginService
    group_service: IGroupService
    settings_service: ISettingsService
    assistant_service: IAssistantService
