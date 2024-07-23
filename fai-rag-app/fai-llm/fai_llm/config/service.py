from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings, extra='ignore'):
    LISTEN_ADDRESS: str = '0.0.0.0'
    LISTEN_PORT: int = 8001
    LOG_LEVEL: str = 'info'
    LOG_FORMAT: str = '%(asctime)s:%(name)s:%(process)d:%(thread)d:%(levelname)s:%(message)s'
    LOG_STDOUT: bool = True

    class Config:
        env_file = '.env'


settings = Settings()
