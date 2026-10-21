
import streamlit as st

from src.incident_response import IncidentResponse


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


response_system = load_response_system()

st.subheader("Server Information")

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

