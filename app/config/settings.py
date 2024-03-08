from functools import lru_cache
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / "dev" / ".env", extra="ignore")

    APP_NAME: str = "openvpc"
    ROOT_PATH: str = ""
    ENVIRONMENT: str = "dev"
    TESTING: bool = False

    # Database
    DB_URL: str
    DB_TEST_URL: str = "sqlite://:memory:"

    # Netbox
    NETBOX_URL: str
    NETBOX_KEY: str
    NETBOX_DEFAULT_ROLE: int = 4  # VPC


@lru_cache()
def get_settings():
    logger.info("Loading application config")
    return Settings()
