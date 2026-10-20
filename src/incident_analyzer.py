
def analyze_server(server):
    required_fields = [
        "server_id",
        "cpu_usage",
        "memory_usage",
        "status"
    ]

    for field in required_fields:
        if field not in server:
            raise ValueError(f"Missing required field: {field}")

    for field in ["cpu_usage", "memory_usage"]:
        value = server[field]

        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not 0 <= value <= 100
        ):
            raise ValueError(
                f"{field} must be a number between 0 and 100"
            )

    if server["status"] not in ["running", "stopped"]:
        raise ValueError("Invalid server status")

    issues = []

    if server["status"] == "stopped":
        issues.append("Server is not running")

    if server["cpu_usage"] > 80:
        issues.append("High CPU usage")

    if server["memory_usage"] > 90:
        issues.append("High memory usage")

    return {
        "server_id": server["server_id"],
        "status": "Incident" if issues else "Healthy",
        "issues": issues
    }
