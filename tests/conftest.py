from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("TESTING", "True")
    monkeypatch.setenv("DATABASE_URL", "sqlite://:memory:")


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as test_client:
        yield test_client
