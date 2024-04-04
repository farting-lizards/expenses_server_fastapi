from typing import cast
from fastapi.testclient import TestClient

from expenses_server.dtos.expenses import ExpenseDTO


def test_get_all_expenses(test_expenses: tuple[TestClient, list[ExpenseDTO]]) -> None:
    client, mock_expenses = test_expenses
    response = client.get("/expenses")
    assert response.status_code == 200
    expenses = cast(list[ExpenseDTO], response.json())
    assert len(expenses) >= len(mock_expenses)
    assert mock_expenses[0] in expenses
    assert mock_expenses[1] in expenses
