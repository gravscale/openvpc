from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import close_db, init_db
from .router import init_routers

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.add("../log/openvpc_{time:YYYY-MM-DD}.log", level="INFO")

    logger.info("Starting up database...")
    await init_db()

    yield

    logger.info("Shutting down database...")
    await close_db()


app = FastAPI(lifespan=lifespan, title=settings.APP_NAME, root_path=settings.ROOT_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
    allow_headers=settings.CORS_HEADERS,
)

init_routers(app)
