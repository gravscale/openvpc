from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from routers import include_routers_from_directory
from settings import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.add("log/register.log", rotation="10 MB")

    logger.info("Starting up routers...")
    await include_routers_from_directory(app, "routes")

    yield

    logger.info("Shutting down...")


app = FastAPI(lifespan=lifespan, root_path=settings.ROOT_PATH)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("openvpc.main:app", host="0.0.0.0", port=8000, reload=True)
