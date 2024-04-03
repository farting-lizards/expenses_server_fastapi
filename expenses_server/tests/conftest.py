from typing import Generator
from fastapi.testclient import TestClient
import pytest
from expenses_server.main import app


@pytest.fixture()
def test_client() -> Generator[TestClient, None, None]:
    client = TestClient(app=app, base_url="http://localhost:8000")
    yield client
