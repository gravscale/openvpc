from fastapi import FastAPI
from loguru import logger

from .settings import get_settings

settings = get_settings()
logger.info("Application is running")


def init_app(lifespan=None) -> FastAPI:
    """
    This function is to initialize the application and all configurations.
    """

    return FastAPI(
        lifespan=lifespan,
        title=settings.APP_NAME,
        root_path=settings.ROOT_PATH,
    )
