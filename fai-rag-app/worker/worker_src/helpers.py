import os
from dotenv import load_dotenv

load_dotenv()


def get_config() -> dict[str, str | bool]:
    def str_to_bool(s: str) -> bool:
        return s.lower() in ("y", "yes", "true", "1")

    get_env = os.getenv

    return {
        "REDIS_HOST": get_env("REDIS_HOST", "redis"),
        "REDIS_PORT": get_env("REDIS_PORT", 6379),
        "REDIS_USERNAME": get_env("REDIS_USERNAME", None),
        "REDIS_PASSWORD": get_env("REDIS_PASSWORD", None),
        "REDIS_LOG_LEVEL": get_env("REDIS_LOG_LEVEL", "INFO"), }


config = get_config()
