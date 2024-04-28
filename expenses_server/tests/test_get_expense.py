from typing import Any
from fastapi.testclient import TestClient


def test_get_expense(test_expenses: tuple[TestClient, list[dict[str, Any]]]) -> None:
    client, mock_expenses = test_expenses
    expense_id = mock_expenses[0]["id"]
    response = client.get(f"/api/expenses/{expense_id}")
    assert response.status_code == 200
    assert response.json() == mock_expenses[0]
