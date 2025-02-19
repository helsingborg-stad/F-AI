from enum import Enum


class AuthenticationType(Enum):
    API_KEY = 'api_key'
    BEARER_TOKEN = 'bearer_token'
