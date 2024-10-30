import jwt
from pydantic_settings import BaseSettings

from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    GEN_PRIVATE_KEY_PATH: str

    class Config:
        env_file = ".env"
        extra = "ignore"


def main() -> None:
    settings = Settings()

    if not settings.GEN_PRIVATE_KEY_PATH:
        return None

    private_key = open(settings.GEN_PRIVATE_KEY_PATH).read()
    token = jwt.encode({'helsingborg-stad': 'folkets-ai'}, private_key, algorithm='RS256')
    print(f"\nGenerated token:\n\n{token}\n")


if __name__ == "__main__":
    main()
