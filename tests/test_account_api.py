from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_authenticated_account_endpoints_require_bearer_token():
    for path in ("/api/v1/me", "/api/v1/profile"):
        response = client.get(path)
        assert response.status_code == 401
        assert response.headers["www-authenticate"] == "Bearer"


def test_profile_update_requires_authentication():
    response = client.patch("/api/v1/profile", json={"full_name": "Taylor Candidate"})
    assert response.status_code == 401


def test_profile_rejects_unrecognized_fields_before_database_access():
    response = client.patch(
        "/api/v1/profile",
        headers={"Authorization": "Bearer test-token"},
        json={"user_id": "another-user", "full_name": "Taylor Candidate"},
    )
    # The auth dependency is evaluated after request validation.
    assert response.status_code == 422
