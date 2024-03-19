from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from .config import get_settings
from .config_set import router as config_router
from .credential import router as credential_router
from .database import close_db, init_db
from .device import router as device_router
from .router import router as router_router
from .vpc import router as vpc_router
from .zone import router as zone_router

settings = get_settings()
logger.add("../log/openvpc_{time:YYYY-MM-DD}.log", level="INFO")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up database...")
    await init_db(app)

    yield

    logger.info("Shutting down database...")
    await close_db()


app = FastAPI(
    lifespan=lifespan,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    root_path=settings.ROOT_PATH,
    debug=settings.ENVIRONMENT.is_debug,
)


app.add_middleware(
    CORSMiddleware,
    allow_headers=settings.CORS_HEADERS,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGINS_REGEX,
    allow_credentials=True,
    allow_methods=("GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"),
)


@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(credential_router.router, prefix="/admin/credential")
app.include_router(zone_router.router, prefix="/admin/zone")
app.include_router(device_router.router, prefix="/admin/device")
app.include_router(config_router.router, prefix="/admin/configuration")
app.include_router(vpc_router.router, prefix="/vpc")
app.include_router(router_router.router, prefix="/router")
