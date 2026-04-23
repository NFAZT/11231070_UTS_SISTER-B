from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_publish_and_dedup():
    event = [{
        "topic": "test",
        "event_id": "123",
        "timestamp": "2026-01-01T10:00:00",
        "source": "me",
        "payload": {}
    }]

    client.post("/publish", json=event)
    client.post("/publish", json=event)

    stats = client.get("/stats").json()

    assert stats["unique_processed"] == 1
    assert stats["duplicate_dropped"] >= 1


def test_invalid_event():
    response = client.post("/publish", json=[{"topic": "x"}])
    assert response.status_code == 422