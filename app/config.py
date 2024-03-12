from functools import lru_cache
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    APP_NAME: str = "openvpc"
    ROOT_PATH: str = ""
    ENVIRONMENT: str = "dev"
    TESTING: bool = False
    DATABASE_URL: str

    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None
    CORS_HEADERS: list[str]

    # Netbox
    NETBOX_URL: str
    NETBOX_KEY: str
    NETBOX_DEFAULT_DEVICE_ROLE: int = 4  # VPC
    NETBOX_DEFAULT_SITE_REGION: int = 2  # São Paulo - Brazil
    NETBOX_DEFAULT_SITE_GROUP: int = 1  # Datacluster - São Paulo - Brazil


@lru_cache()
def get_settings():
    logger.info("Loading application config")
    return Config()
