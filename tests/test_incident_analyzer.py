
from src.incident_analyzer import analyze_server


def test_high_cpu_is_detected():
    server = {
        "server_id": "test-01",
        "cpu_usage": 95,
        "memory_usage": 50,
        "status": "running"
    }

    result = analyze_server(server)

    assert result["status"] == "Incident"
    assert "High CPU usage" in result["issues"]


def test_healthy_server():
    server = {
        "server_id": "test-02",
        "cpu_usage": 30,
        "memory_usage": 40,
        "status": "running"
    }

    result = analyze_server(server)

    assert result["status"] == "Healthy"
    assert result["issues"] == []


def test_stopped_server():
    server = {
        "server_id": "test-03",
        "cpu_usage": 10,
        "memory_usage": 20,
        "status": "stopped"
    }

    result = analyze_server(server)

    assert result["status"] == "Incident"
    assert "Server is not running" in result["issues"]


def test_high_memory_is_detected():
    server = {
        "server_id": "test-04",
        "cpu_usage": 40,
        "memory_usage": 96,
        "status": "running"
    }

    result = analyze_server(server)

    assert result["status"] == "Incident"
    assert "High memory usage" in result["issues"]



import pytest


def test_invalid_cpu_is_rejected():
    server = {
        "server_id": "test-05",
        "cpu_usage": 150,
        "memory_usage": 50,
        "status": "running"
    }

    with pytest.raises(ValueError):
        analyze_server(server)
