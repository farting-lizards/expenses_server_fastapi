from typing import Any
from fastapi.testclient import TestClient
import copy


def test_update_expense(test_expenses: tuple[TestClient, list[dict[str, Any]]]) -> None:
    client, mock_expenses = test_expenses
    expense_before_update = mock_expenses[0]

    payload = {
        "amount": 10.89,
    }
    expected_response = copy.deepcopy(expense_before_update)
    expected_response.update(payload)

    response = client.patch(
        f"/api/expenses/{expense_before_update["id"]}", json=payload
    )
    assert response.status_code == 200
    actual_response = response.json()
    assert actual_response == expected_response
