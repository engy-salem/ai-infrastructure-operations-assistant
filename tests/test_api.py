
from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert "API is running" in response.json()["message"]


def test_analyze_high_cpu_server():
    response = client.post(
        "/analyze",
        json={
            "server_id": "test-01",
            "cpu_usage": 95,
            "memory_usage": 50,
            "status": "running",
        },
    )

    assert response.status_code == 200

    report = response.json()
    assert report["status"] == "Incident"
    assert report["issues"][0]["runbook_id"] == "RB001"


def test_analyze_healthy_server():
    response = client.post(
        "/analyze",
        json={
            "server_id": "test-02",
            "cpu_usage": 30,
            "memory_usage": 40,
            "status": "running",
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Healthy"
    assert response.json()["issues"] == []


def test_reject_invalid_cpu():
    response = client.post(
        "/analyze",
        json={
            "server_id": "test-03",
            "cpu_usage": 150,
            "memory_usage": 40,
            "status": "running",
        },
    )

    assert response.status_code == 422

