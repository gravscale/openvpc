from functools import lru_cache

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

from .constants import Environment


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "openvpc"
    APP_VERSION: str = "1"
    ROOT_PATH: str = ""

    DATABASE_URL: str

    ENVIRONMENT: Environment = Environment.LOCAL

    CORS_HEADERS: list[str]
    CORS_ORIGINS: list[str]
    CORS_ORIGINS_REGEX: str | None = None

    # Netbox
    NETBOX_URL: str
    NETBOX_KEY: str
    NETBOX_ROUTER_ROLE: int = 2  # router
    NETBOX_DEVICE_ROLE: int = 4  # VPC
    NETBOX_DEFAULT_SITE_REGION: int = 2  # São Paulo - Brazil
    NETBOX_DEFAULT_SITE_GROUP: int = 1  # Datacluster - São Paulo - Brazil


@lru_cache()
def get_settings():
    logger.info("Loading application config.")
    return Config()
