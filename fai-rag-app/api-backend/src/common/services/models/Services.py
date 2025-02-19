from dataclasses import dataclass

from src.modules.api_key.protocols.IApiKeyService import IApiKeyService
from src.modules.auth.authentication.factory import AuthenticationServiceFactory
from src.modules.auth.authorization.protocols.IAuthorizationService import IAuthorizationService
from src.modules.llm.protocols.ILLMService import ILLMService


@dataclass
class Services:
    authentication_factory: AuthenticationServiceFactory
    authorization_service: IAuthorizationService
    api_key_service: IApiKeyService
    llm_service: ILLMService
