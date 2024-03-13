from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.configuration import router as config_router
from app.credential import router as credential_router
from app.device import router as device_router
from app.vpc import router as vpc_router
from app.zone import router as zone_router

from .config import get_settings
from .database import close_db, init_db

# from app.router import router as router_router


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


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(credential_router.router, prefix="/admin/credential")
app.include_router(zone_router.router, prefix="/admin/zone")
app.include_router(device_router.router, prefix="/admin/device")
app.include_router(config_router.router, prefix="/admin/configuration")
# app.include_router(router_router.router, prefix="/router")
app.include_router(vpc_router.router, prefix="/vpc")
