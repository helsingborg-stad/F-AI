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

    class Config:
        env_file = '.env'


settings = Settings()
