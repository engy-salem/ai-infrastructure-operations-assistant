
def analyze_server(server):
    issues = []

    if server["status"] != "running":
        issues.append("Server is not running")

    if server["cpu_usage"] > 80:
        issues.append("High CPU usage")

    if server["memory_usage"] > 90:
        issues.append("High memory usage")

    if not issues:
        return {
            "server_id": server["server_id"],
            "status": "Healthy",
            "issues": []
        }

    return {
        "server_id": server["server_id"],
        "status": "Incident",
        "issues": issues
    }

