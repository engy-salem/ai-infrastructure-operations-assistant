import pytest

from src.incident_response import IncidentResponse


@pytest.fixture(scope="module")
def response_system():
    return IncidentResponse()


def test_process_server_finds_cpu_runbook(response_system):
    server = {
        "server_id": "test-01",
        "cpu_usage": 95,
        "memory_usage": 50,
        "status": "running"
    }

    report = response_system.process_server(server)

    assert report["server_id"] == "test-01"
    assert report["status"] == "Incident"
    assert report["issues"][0]["runbook_found"] is True
    assert report["issues"][0]["runbook_id"] == "RB001"


def test_healthy_server_has_no_issues(response_system):
    server = {
        "server_id": "test-02",
        "cpu_usage": 30,
        "memory_usage": 40,
        "status": "running"
    }

    report = response_system.process_server(server)

    assert report["status"] == "Healthy"
    assert report["issues"] == []
