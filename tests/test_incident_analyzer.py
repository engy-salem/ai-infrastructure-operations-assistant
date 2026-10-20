
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


from src.runbook_retriever import load_runbooks, find_runbook


def test_load_runbooks():
    runbooks = load_runbooks()

    assert len(runbooks) == 3


def test_find_cpu_runbook():
    runbook = find_runbook("High CPU usage")

    assert runbook is not None
    assert runbook["id"] == "RB001"


def test_find_memory_runbook():
    runbook = find_runbook("High memory usage")

    assert runbook is not None
    assert runbook["id"] == "RB002"


def test_unknown_issue_returns_none():
    runbook = find_runbook("Unknown issue")

    assert runbook is None


from src.semantic_search import SemanticSearch


def test_semantic_search_finds_cpu_runbook():
    search_engine = SemanticSearch()

    result = search_engine.search(
        "The processor is using too many resources"
    )

    assert result["found"] is True
    assert result["runbook"]["id"] == "RB001"


def test_semantic_search_finds_memory_runbook():
    search_engine = SemanticSearch()

    result = search_engine.search(
        "The machine has almost no free memory"
    )

    assert result["found"] is True
    assert result["runbook"]["id"] == "RB002"


def test_semantic_search_rejects_unrelated_query():
    search_engine = SemanticSearch()

    result = search_engine.search(
        "How can I improve my website design?"
    )

    assert result["found"] is False


def test_semantic_search_rejects_empty_query():
    search_engine = SemanticSearch()

    with pytest.raises(ValueError):
        search_engine.search("   ")
