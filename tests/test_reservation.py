import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).parent.parent / "services" / "reservation-service")
)

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_reservation():
    response = client.post(
        "/reservations",
        json={
            "customer_name": "Test User",
            "resource": "Sala Test",
            "reservation_date": "2026-12-01T10:00:00"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer_name"] == "Test User"
    assert data["resource"] == "Sala Test"
    assert "id" in data


def test_list_reservations():
    response = client.get("/reservations")

    assert response.status_code == 200
    assert isinstance(response.json(), list)