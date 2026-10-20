
from src.incident_analyzer import analyze_server
from src.semantic_search import SemanticSearch


class IncidentResponse:
    def __init__(self, threshold=0.35):
        self.search_engine = SemanticSearch(threshold=threshold)

    def process_server(self, server):
        analysis = analyze_server(server)

        report = {
            "server_id": analysis["server_id"],
            "status": analysis["status"],
            "issues": []
        }

        for issue in analysis["issues"]:
            result = self.search_engine.search(issue)

            issue_report = {
                "issue": issue,
                "runbook_found": result["found"]
            }

            if result["found"]:
                runbook = result["runbook"]

                issue_report["runbook_id"] = runbook["id"]
                issue_report["runbook_title"] = runbook["title"]
                issue_report["troubleshooting_steps"] = (
                    runbook["troubleshooting_steps"]
                )
            else:
                issue_report["message"] = result["message"]

            report["issues"].append(issue_report)

        return report

