import os
from functools import lru_cache

from dotenv import load_dotenv
from loguru import logger
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, "dev", ".env"))


class Settings(BaseSettings):
    ROOT_PATH: str = os.environ.get("ROOT_PATH", "")
    ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "dev")
    TESTING: bool = os.environ.get("TESTING", False)

    # Database
    MYSQL_HOST: str = os.environ.get("MYSQL_HOST", "127.0.0.1")
    MYSQL_PORT: int = os.environ.get("MYSQL_PORT", 3306)
    MYSQL_USERNAME: str = os.environ.get("MYSQL_USERNAME")
    MYSQL_PASSWORD: str = os.environ.get("MYSQL_PASSWORD")
    MYSQL_DATABASE: str = os.environ.get("MYSQL_DATABASE")

    # VyOS
    VYOS_HOST: str = os.environ.get("VYOS_HOST")
    VYOS_PORT: int = os.environ.get("VYOS_PORT")
    VYOS_KEY: str = os.environ.get("VYOS_KEY")


@lru_cache()
def get_settings():
    logger.info("Loading application config")
    return Settings()
