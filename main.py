
from src.server_monitor import servers
from src.incident_analyzer import analyze_server


def main():
    for server in servers:
        result = analyze_server(server)

        print(f"\nServer: {result['server_id']}")
        print(f"Status: {result['status']}")

        for issue in result["issues"]:
            print(f"- {issue}")

        if not result["issues"]:
            print("- No issues detected")


if __name__ == "__main__":
    main()

