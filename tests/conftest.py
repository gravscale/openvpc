import asyncio

import pytest
from fastapi.testclient import TestClient

from app.config.bootstrap import init_app
from app.config.db import close_db, init_db
from app.config.routers import init_routers
from app.config.settings import get_settings

settings = get_settings()
settings.TESTING = True


def start_all_inits(app):
    asyncio.run(init_routers(app))
    asyncio.run(init_db())


def close_all_inits():
    asyncio.run(close_db())


@pytest.fixture(scope="module")
def client():
    app = init_app()
    start_all_inits(app)

    with TestClient(app) as test_client:
        yield test_client

    close_all_inits()
