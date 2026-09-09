from fastapi.testclient import TestClient
from traveler_service.app import app as traveler_app

client = TestClient(traveler_app)

def test_unknown_traveler_returns_404():
    response = client.get(
        "/internal/travelers/T-9999",
        headers={
            "X-User-Id": "demo-user",
            "X-User-Role": "officer",
            "X-User-Office": "JFK",
            "X-Internal-Key": "demo-internal-key",
        },
    )
    assert response.status_code == 404

def test_officer_cannot_read_other_office_record():
    response = client.get(
        "/internal/travelers/T-1001",
        headers={
            "X-User-Id": "demo-user",
            "X-User-Role": "officer",
            "X-User-Office": "IAD",
            "X-Internal-Key": "demo-internal-key",
        },
    )
    assert response.status_code == 403
