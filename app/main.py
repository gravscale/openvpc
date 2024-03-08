from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from .config.bootstrap import init_app
from .config.db import close_db, init_db
from .config.routers import init_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.add("../log/openvpc_{time:YYYY-MM-DD}.log", level="INFO")

    logger.info("Starting up routers...")
    await init_routers(app)

    logger.info("Starting up database...")
    await init_db()

    yield

    logger.info("Shutting down database...")
    await close_db()


app = init_app(lifespan)

if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True, lifespan="on")
