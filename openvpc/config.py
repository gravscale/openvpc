from functools import lru_cache
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / "dev" / ".env")

    ROOT_PATH: str = ""
    ENVIRONMENT: str = "dev"
    TESTING: bool = False

    # Database
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3306
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str

    # Netbox
    NETBOX_URL: str
    NETBOX_KEY: str
    NETBOX_DEFAULT_ROLE: int = 4  # VPC


@lru_cache()
def get_settings():
    logger.info("Loading application config")
    return Settings()
