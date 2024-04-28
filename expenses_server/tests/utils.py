from typing import Any, cast
from fastapi.testclient import TestClient


def create_mock_expense(
    client: TestClient, extra: dict[str, Any] | None = None
) -> dict[str, Any]:
    payload = (
        {
            "amount": 10,
            "currency": "CHF",
            "description": "Migros",
            "category_name": "groceries",
            "account_id": 1,
        }
        if extra is None
        else {
            "amount": 10,
            "currency": "CHF",
            "description": "Migros",
            "category_name": "groceries",
            "account_id": 1,
            **extra,
        }
    )
    response = client.post("/api/expenses", json=payload)
    assert response.status_code == 200
    return cast(dict[str, Any], response.json())
