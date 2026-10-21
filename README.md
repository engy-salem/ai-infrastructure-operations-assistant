# AI Infrastructure Operations Assistant

An AI-powered infrastructure monitoring and incident response assistant that analyzes server health metrics, identifies potential operational issues, and retrieves relevant troubleshooting procedures using semantic search.

## Overview

The AI Infrastructure Operations Assistant helps identify common infrastructure issues and provides relevant troubleshooting guidance based on a collection of operational runbooks.

The system combines rule-based server health analysis with semantic search to connect detected incidents to relevant troubleshooting documentation.

This project demonstrates the application of AI and software engineering techniques to infrastructure operations and incident management.

## Key Features

- **Server Health Analysis:** Evaluates CPU and memory utilization to identify potential infrastructure issues.
- **Incident Detection:** Identifies server incidents, including high CPU usage, high memory utilization, and stopped or unhealthy server states.
- **Semantic Runbook Search:** Uses sentence embeddings and semantic similarity to retrieve troubleshooting procedures relevant to a detected incident.
- **Relevance Filtering:** Rejects irrelevant queries when no sufficiently relevant runbook is found.
- **Incident Response Pipeline:** Integrates server analysis, incident identification, and runbook retrieval into a structured response.
- **REST API:** Provides FastAPI endpoints for health checks and server analysis.
- **Automated Testing:** Uses pytest to validate core functionality, input validation, semantic search, and incident response behavior.

## Technology Stack

- **Programming Language:** Python
- **AI / NLP:** Sentence Transformers, text embeddings, semantic similarity search
- **Backend:** FastAPI
- **Data Processing:** NumPy
- **Testing:** pytest, HTTPX
- **Data Storage:** JSON-based troubleshooting runbooks

## System Architecture

The application follows a modular architecture:

1. **Input Layer:** Receives server identifiers and infrastructure metrics.
2. **Health Analysis:** Evaluates the provided metrics and identifies potential incidents.
3. **Incident Response:** Generates a structured incident report.
4. **Semantic Retrieval:** Searches the runbook collection using semantic similarity.
5. **Troubleshooting Guidance:** Returns relevant procedures when a sufficiently similar runbook is found.
6. **API Layer:** Exposes the functionality through REST endpoints.

```text
Server Metrics
      |
      v
Input Validation
      |
      v
Server Health Analysis
      |
      v
Incident Detection
      |
      v
Semantic Runbook Search
      |
      v
Relevance Filtering
      |
      v
Incident Report and
Troubleshooting Guidance
      |
      v
FastAPI Response
```

## Project Structure

```text
ai-infrastructure-operations-assistant/
├── data/
│   └── runbooks.json
├── src/
│   ├── semantic_search.py
│   ├── incident_response.py
│   └── api.py
├── tests/
│   └── test_incident_response.py
├── AI_Infrastructure_Operations_Assistant.ipynb
├── requirements.txt
└── README.md
```

Additional test files may be present in the `tests/` directory.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/engy-salem/ai-infrastructure-operations-assistant.git
cd ai-infrastructure-operations-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the Application

Start the FastAPI development server:

```bash
uvicorn src.api:app --reload
```

Open the interactive API documentation in your browser:

```text
http://127.0.0.1:8000/docs
```

### Available Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application health check |
| POST | `/analyze` | Analyze server metrics and generate an incident response |

### Example API Request

Send a POST request to `/analyze` with a JSON payload matching the API input schema:

```json
{
  "server_id": "server-01",
  "cpu_usage": 92,
  "memory_usage": 65
}
```

The exact field names must match the Pydantic model implemented in `src/api.py`.

The response is designed to provide a structured analysis of the server and relevant troubleshooting information when an incident is detected.

## Run Tests

Run the automated test suite from the project root:

```bash
python -m pytest -v
```

The test suite covers core server health validation, incident detection, runbook matching, semantic search relevance, and incident response integration.

## Example Use Case

When a server experiences unusually high CPU utilization, the system can identify the potential incident and search the runbook collection for relevant troubleshooting guidance.

For example, a high-CPU incident may be associated with the **High CPU Usage** runbook, which contains possible causes and troubleshooting steps.

If a query is unrelated to the available runbooks, the semantic retrieval component can reject the match instead of returning an irrelevant procedure.

## Engineering Highlights

- Modular separation of server analysis, semantic retrieval, and API functionality.
- Embedding-based semantic matching for operational documentation.
- Input validation and automated regression testing.
- Relevance filtering to reduce unrelated retrieval results.
- REST API integration for programmatic access.

## Future Improvements

- Integration with live infrastructure monitoring systems.
- Support for additional server metrics and incident categories.
- Integration with observability platforms and alerting systems.
- Retrieval evaluation using metrics such as Recall@K and Mean Reciprocal Rank (MRR).
- Containerization and deployment to a cloud environment.



