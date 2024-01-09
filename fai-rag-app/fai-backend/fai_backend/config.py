from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_DB: str = 'memory'
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENV_MODE: str = 'development'

    MONGO_DB_NAME: str
    MONGO_DB_URI: str = 'mongodb://localhost:27017'
    FIXED_PIN: int | None = None

    APP_PROJECT_NAME: str
    APP_ADMIN_EMAIL: str

    MAIL_CLIENT: str
    MAIL_SENDER_EMAIL: str
    MAIL_SENDER_NAME: str

    BREVO_API_URL: str
    BREVO_API_KEY: str

    LOG_LEVEL: str

    class Config:
        env_file = '.env'


settings = Settings()
