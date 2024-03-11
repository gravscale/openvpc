import asyncio

import pytest
from fastapi.testclient import TestClient

from app.bootstrap import init_app
from app.config import get_settings
from app.database import close_db, init_test_db
from app.router import init_routers

settings = get_settings()
settings.TESTING = True


def start_all_inits(app):
    init_routers(app)
    asyncio.run(init_test_db())


def close_all_inits():
    asyncio.run(close_db())


@pytest.fixture(scope="module")
def client():
    app = init_app()
    start_all_inits(app)

    with TestClient(app) as test_client:
        yield test_client

    close_all_inits()
