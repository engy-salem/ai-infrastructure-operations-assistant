
import streamlit as st

from src.incident_response import IncidentResponse
from src.semantic_search import SemanticSearch


st.set_page_config(
    page_title="AI Infrastructure Operations Assistant",
    page_icon="🖥️",
    layout="wide",
)

st.title("AI Infrastructure Operations Assistant")
st.write(
    "Monitor server health, detect incidents, "
    "and retrieve relevant troubleshooting steps."
)


@st.cache_resource
def load_response_system():
    return IncidentResponse()


@st.cache_resource
def load_semantic_search():
    return SemanticSearch()


response_system = load_response_system()

st.header("1. Server Health Analysis")

with st.form("server_form"):
    server_id = st.text_input("Server ID", value="server-01")
    cpu_usage = st.slider("CPU Usage (%)", 0, 100, 50)
    memory_usage = st.slider("Memory Usage (%)", 0, 100, 50)
    status = st.selectbox("Server Status", ["running", "stopped"])

    submitted = st.form_submit_button("Analyze Server")

if submitted:
    if not server_id.strip():
        st.error("Please enter a Server ID.")
    else:
        server = {
            "server_id": server_id.strip(),
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "status": status,
        }

        try:
            report = response_system.process_server(server)

            st.subheader("Analysis Report")
            st.write(f"**Server:** {report['server_id']}")

            if report["status"] == "Healthy":
                st.success("Server is Healthy")
            else:
                st.error("Incident Detected")

            if not report["issues"]:
                st.info("No issues detected.")
            else:
                for issue in report["issues"]:
                    st.markdown(f"### {issue['issue']}")

                    if issue["runbook_found"]:
                        st.write(
                            f"**Runbook:** {issue['runbook_id']} — "
                            f"{issue['runbook_title']}"
                        )

                        st.write("**Troubleshooting Steps:**")
                        for step in issue["troubleshooting_steps"]:
                            st.markdown(f"- {step}")
                    else:
                        st.warning(
                            issue.get(
                                "message",
                                "No relevant runbook was found.",
                            )
                        )

        except (ValueError, KeyError) as error:
            st.error(f"Could not analyze server: {error}")


st.divider()
st.header("2. Semantic Runbook Search")

st.write(
    "Describe an infrastructure problem in your own words "
    "to find the most relevant troubleshooting runbook."
)

with st.form("semantic_search_form"):
    query = st.text_area(
        "Describe the problem",
        placeholder=(
            "Example: The server is running slowly "
            "and applications are responding late."
        ),
    )

    search_submitted = st.form_submit_button("Find Relevant Runbook")

if search_submitted:
    if not query.strip():
        st.warning("Please describe the problem first.")
    else:
        try:
            with st.spinner("Searching for relevant runbooks..."):
                semantic_search = load_semantic_search()
                result = semantic_search.search(query)

            if result["found"]:
                runbook = result["runbook"]

                st.success("Relevant runbook found!")

                runbook_id = runbook.get(
                    "id",
                    runbook.get("runbook_id", "N/A"),
                )

                st.subheader(
                    f"{runbook_id} — {runbook['title']}"
                )

                st.write(
                    f"**Similarity score:** {result['similarity']}"
                )

                if runbook.get("problem"):
                    st.write(f"**Problem:** {runbook['problem']}")

                if runbook.get("possible_causes"):
                    st.write("**Possible Causes:**")
                    for cause in runbook["possible_causes"]:
                        st.markdown(f"- {cause}")

                st.write("**Troubleshooting Steps:**")
                for step in runbook["troubleshooting_steps"]:
                    st.markdown(f"- {step}")

            else:
                st.warning(result["message"])
                st.write(
                    f"Similarity score: {result['similarity']}"
                )

        except (ValueError, KeyError) as error:
            st.error(f"Could not search runbooks: {error}")
        except Exception as error:
            st.error(f"Search failed: {error}")
