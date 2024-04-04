from typing import Any, cast
from fastapi.testclient import TestClient

from expenses_server.dtos.expenses import ExpenseDTO


def create_mock_expense(
    client: TestClient, extra: dict[str, Any] | None = None
) -> ExpenseDTO:
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
    response = client.post("/expenses", json=payload)
    assert response.status_code == 200
    return cast(ExpenseDTO, response.json())
