from typing import Generator

import pytest
from fastapi.testclient import TestClient
from starlette.config import environ

environ["TESTING"] = "True"
environ["DATABASE_URL"] = "sqlite://:memory:"

from app.main import app  # noqa

pytest_plugins = ["tests.fixtures"]


@pytest.fixture(scope="session")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as client:
        yield client
