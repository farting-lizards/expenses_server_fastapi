from http import HTTPStatus
from typing import Any, Generator
from fastapi.testclient import TestClient
import pytest
from expenses_server.main import app
from expenses_server.db import SessionLocal
from expenses_server.db_models.expense import Expense
from expenses_server.db_models.user import User
from expenses_server.utils import hash_password
from expenses_server.tests.utils import create_mock_expense

TEST_USERNAME = "pinkie"
TEST_PASSWORD = "floydian"


@pytest.fixture(autouse=True)
def cleanup_created_expenses() -> Generator[None, None, None]:
    session = SessionLocal()
    existing_ids = {expense_id for (expense_id,) in session.query(Expense.id)}

    yield

    session.query(Expense).filter(Expense.id.not_in(existing_ids)).delete()
    session.commit()
    session.close()


@pytest.fixture()
def test_user() -> Generator[User, None, None]:
    session = SessionLocal()
    # Clean up leftovers from previously aborted runs
    session.query(User).filter(User.username == TEST_USERNAME).delete()
    user = User(username=TEST_USERNAME, password_hash=hash_password(TEST_PASSWORD))
    session.add(user)
    session.commit()

    yield user

    session.delete(user)
    session.commit()
    session.close()


@pytest.fixture()
def anonymous_client() -> Generator[TestClient, None, None]:
    client = TestClient(app=app, base_url="http://localhost:8090")
    yield client


@pytest.fixture()
def test_client(
    anonymous_client: TestClient, test_user: User
) -> Generator[TestClient, None, None]:
    response = anonymous_client.post(
        "/api/users/token",
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD},
    )
    assert response.status_code == HTTPStatus.OK
    token = response.json()["access_token"]
    anonymous_client.headers["Authorization"] = f"Bearer {token}"
    yield anonymous_client


@pytest.fixture()
def test_expenses(
    test_client: TestClient,
) -> Generator[tuple[TestClient, list[dict[str, Any]]], None, None]:
    expense1 = create_mock_expense(test_client)
    expense2 = create_mock_expense(test_client, extra={"account_id": 2})

    yield test_client, [expense1, expense2]
