from http import HTTPStatus

from fastapi.testclient import TestClient

from expenses_server.db_models.user import User
from expenses_server.tests.conftest import TEST_PASSWORD, TEST_USERNAME


def test_login_returns_token(anonymous_client: TestClient, test_user: User) -> None:
    response = anonymous_client.post(
        "/api/users/token",
        data={"username": TEST_USERNAME, "password": TEST_PASSWORD},
    )
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_login_with_wrong_password(
    anonymous_client: TestClient, test_user: User
) -> None:
    response = anonymous_client.post(
        "/api/users/token",
        data={"username": TEST_USERNAME, "password": "wrong"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_login_with_unknown_user(anonymous_client: TestClient) -> None:
    response = anonymous_client.post(
        "/api/users/token",
        data={"username": "who-is-this", "password": TEST_PASSWORD},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_protected_routes_require_token(anonymous_client: TestClient) -> None:
    for path in ["/api/expenses", "/api/accounts", "/api/users/me"]:
        response = anonymous_client.get(path)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, path


def test_invalid_token_is_rejected(anonymous_client: TestClient) -> None:
    anonymous_client.headers["Authorization"] = "Bearer not-a-real-token"
    response = anonymous_client.get("/api/expenses")
    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_me_does_not_leak_password_hash(test_client: TestClient) -> None:
    response = test_client.get("/api/users/me")
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["username"] == TEST_USERNAME
    assert "password_hash" not in body
