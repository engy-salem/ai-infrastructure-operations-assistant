
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.incident_response import IncidentResponse


app = FastAPI(
    title="AI Infrastructure Operations Assistant",
    description="API for server incident detection and troubleshooting.",
    version="1.0.0",
)

response_system = IncidentResponse()


class ServerData(BaseModel):
    server_id: str = Field(min_length=1)
    cpu_usage: float = Field(ge=0, le=100)
    memory_usage: float = Field(ge=0, le=100)
    status: str


@app.get("/")
def home():
    return {
        "message": "AI Infrastructure Operations Assistant API is running"
    }


@app.post("/analyze")
def analyze_server_endpoint(server: ServerData):
    try:
        return response_system.process_server(server.model_dump())
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

