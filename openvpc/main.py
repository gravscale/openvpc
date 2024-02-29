from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from .config import get_settings
from .database import init_db, stop_db
from .routers import include_routers_from_directory

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.add("log/openvpc_{time:YYYY-MM-DD}.log", level="INFO")

    logger.info("Starting up routers...")
    await include_routers_from_directory(app, "routes")

    logger.info("Starting up database...")
    await init_db()

    yield

    logger.info("Shutting down database...")
    await stop_db()


app = FastAPI(lifespan=lifespan, root_path=settings.ROOT_PATH)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("openvpc.main:app", host="0.0.0.0", port=8000, reload=True)
