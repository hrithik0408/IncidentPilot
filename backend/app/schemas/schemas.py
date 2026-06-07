from typing import Any
from pydantic import BaseModel, Field

class ServiceCreate(BaseModel):
    name: str
    environment: str = "production"
    description: str = ""
    repository_url: str = ""
    healthcheck_url: str = ""
    metadata: dict[str, Any] = Field(default_factory=dict)

class AlertWebhook(BaseModel):
    source: str = "demo-monitor"
    external_alert_id: str = ""
    service: str = "payments-api"
    title: str
    description: str = ""
    severity: str = "critical"
    labels: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, Any] = Field(default_factory=dict)
    timestamp: str | None = None

class AgentRunRequest(BaseModel):
    agent_type: str = "full_investigation"
    mode: str = "assist"

class ApprovalRequest(BaseModel):
    decision_note: str = "Approved by demo responder."

class RunbookCreate(BaseModel):
    service_id: str | None = None
    title: str
    description: str = ""
    content: str
    tags: list[str] = Field(default_factory=list)
