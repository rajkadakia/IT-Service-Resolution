from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

CATEGORIES = ["dns", "vpn", "firewall", "proxy"]


def validate_response_schema(data, category):
    assert "category" in data
    assert "answer" in data
    assert "context" in data

    assert data["category"] == category
    assert isinstance(data["answer"], str)
    assert isinstance(data["context"], list)

    for item in data["context"]:
        assert "incident_id" in item
        assert "text" in item
        assert isinstance(item["incident_id"], str)
        assert isinstance(item["text"], str)


def test_all_category_endpoints():
    """
    This test ensures:
    - All category endpoints are reachable
    - They return HTTP 200
    - They return the correct response shape
    """

    payload = {
        "query": "connection issue"
    }

    for category in CATEGORIES:
        response = client.post(f"/search/{category}", json=payload)

        assert response.status_code == 200

        data = response.json()
        validate_response_schema(data, category)
