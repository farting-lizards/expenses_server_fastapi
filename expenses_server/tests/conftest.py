from http import HTTPStatus
from typing import Generator
from fastapi.testclient import TestClient
import pytest
from expenses_server.main import app
from expenses_server.tests.utils import create_mock_expense


@pytest.fixture()
def test_client() -> Generator[TestClient, None, None]:
    client = TestClient(app=app, base_url="http://localhost:8090")
    yield client


@pytest.fixture()
def test_expenses(
    test_client: TestClient,
) -> Generator[tuple[TestClient, list[dict]], None, None]:
    expense1 = create_mock_expense(test_client)
    print("EXPENSE1", expense1)
    expense2 = create_mock_expense(test_client, extra={"account_id": 2})
    print("EXPENSE2", expense2)

    yield test_client, [expense1, expense2]

    for expense in [expense1, expense2]:
        response = test_client.delete(f'/expenses/{expense["id"]}')
        assert response.status_code in [HTTPStatus.NOT_FOUND, HTTPStatus.OK]
