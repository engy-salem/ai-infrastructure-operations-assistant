
import json
from pathlib import Path


def load_runbooks():
    project_root = Path(__file__).resolve().parent.parent
    runbooks_path = project_root / "data" / "runbooks.json"

    with open(runbooks_path, "r", encoding="utf-8") as file:
        return json.load(file)


def find_runbook(issue):
    runbooks = load_runbooks()

    issue_to_runbook = {
        "High CPU usage": "RB001",
        "High memory usage": "RB002",
        "Server is not running": "RB003",
    }

    runbook_id = issue_to_runbook.get(issue)

    for runbook in runbooks:
        if runbook["id"] == runbook_id:
            return runbook

    return None

