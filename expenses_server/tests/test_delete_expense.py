from http import HTTPStatus
from fastapi.testclient import TestClient


def test_delete_expenses(test_expenses: tuple[TestClient, list[dict]]) -> None:
    client, mock_expenses = test_expenses
    expense_id = mock_expenses[0]["id"]
    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == mock_expenses[0]

    get_deleted_expense = client.get(f"/expenses/{expense_id}")
    assert get_deleted_expense.status_code == HTTPStatus.NOT_FOUND
