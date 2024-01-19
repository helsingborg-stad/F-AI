from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_PROJECT_NAME: str = 'fai-rag-app'
    APP_ADMIN_EMAIL: str
    APP_DB: str = 'mongodb'
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ENV_MODE: str = 'production'
    MONGO_DB_NAME: str = 'fai-rag-app'
    MONGO_DB_URI: str = 'mongodb://localhost:27017'
    FIXED_PIN: int | None = None
    MAIL_CLIENT: str
    MAIL_SENDER_EMAIL: str
    MAIL_SENDER_NAME: str
    BREVO_API_URL: str
    BREVO_API_KEY: str
    LOG_LEVEL: str = 'INFO'
    DEFAULT_LANGUAGE: str = 'en'

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
