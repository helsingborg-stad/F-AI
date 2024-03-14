from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_PROJECT_NAME: str = 'fai-rag-app'
    APP_ADMIN_EMAIL: str
    APP_DB: Literal['memory', 'mongodb'] = 'mongodb'
    APP_VECTOR_DB: Literal['memory', 'chromadb'] = 'chromadb'
    APP_VECTOR_DB_PATH: str = 'vector_db'
    APP_MESSAGE_BROKER: Literal['memory', 'redis_queue'] = 'redis_queue'
    SECRET_KEY: SecretStr
    BREVO_API_URL: str = 'https://api.brevo.com/v3/smtp/email'
    BREVO_API_KEY: SecretStr = 'api-key'
    ALGORITHM: str = 'HS256'
    ENV_MODE: Literal['testing', 'development', 'production'] = 'production'
    MONGO_DB_NAME: str = 'fai-rag-app'
    MONGO_DB_URI: str = 'mongodb://localhost:27017'
    FIXED_PIN: int | None = None
    MAIL_CLIENT: Literal['console', 'brevo'] = 'console'
    MAIL_SENDER_NAME: str = 'FAI App'
    MAIL_SENDER_EMAIL: str = 'no-reply@localhost.dev'
    LOG_LEVEL: str = 'INFO'
    DEFAULT_LANGUAGE: str = 'en'
    FILE_UPLOAD_PATH: str = 'uploads'

    class Config:
        env_file = '.env'


settings = None

try:
    env_settings = Settings()
    if env_settings.ENV_MODE == 'testing':
        raise Exception('Testing mode is enabled')
    else:
        settings = env_settings
except Exception:
    class TestSettings(Settings):
        class Config:
            env_file = '.env.test'


    settings = TestSettings()
