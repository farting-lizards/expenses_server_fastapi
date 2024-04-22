from fastapi.testclient import TestClient


def test_virtual_lab_created(test_client: TestClient) -> None:
    payload = {
        "amount": 10,
        "currency": "CHF",
        "description": "Migros",
        "category_name": "groceries",
        "account_id": 1,
    }
    response = test_client.post("/api/expenses", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["amount"] == 10.0
    assert data["currency"] == "CHF"
    assert data["description"] == "Migros"
    assert data["category"] == "groceries"
    assert data["account"]["id"] == 1
    assert data["account"]["name"] == "Wise David"
