import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.session import Base

def uuid_str() -> str:
    return str(uuid.uuid4())

class Team(Base):
    __tablename__ = "teams"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(50), default="responder")
    password_hash: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Service(Base):
    __tablename__ = "services"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    environment: Mapped[str] = mapped_column(String(50), default="production")
    description: Mapped[str] = mapped_column(Text, default="")
    repository_url: Mapped[str] = mapped_column(Text, default="")
    healthcheck_url: Mapped[str] = mapped_column(Text, default="")
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"), nullable=False)
    service_id: Mapped[str] = mapped_column(String, ForeignKey("services.id"), nullable=True)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False)
    external_alert_id: Mapped[str] = mapped_column(String(255), default="")
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    severity: Mapped[str] = mapped_column(String(50), default="medium")
    status: Mapped[str] = mapped_column(String(50), default="received")
    payload: Mapped[dict] = mapped_column(JSON, default=dict)
    received_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"), nullable=False)
    service_id: Mapped[str] = mapped_column(String, ForeignKey("services.id"), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, default="")
    severity: Mapped[str] = mapped_column(String(50), default="medium")
    status: Mapped[str] = mapped_column(String(50), default="open")
    root_cause: Mapped[str] = mapped_column(Text, default="")
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    detected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    acknowledged_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    resolved_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class IncidentEvent(Base):
    __tablename__ = "incident_events"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=False)
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    actor_type: Mapped[str] = mapped_column(String(50), default="agent")
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class AgentRun(Base):
    __tablename__ = "agent_runs"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=False)
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="running")
    input: Mapped[dict] = mapped_column(JSON, default=dict)
    output: Mapped[dict] = mapped_column(JSON, default=dict)
    model_name: Mapped[str] = mapped_column(String(100), default="qwen-plus")
    prompt_tokens: Mapped[int] = mapped_column(Integer, default=0)
    completion_tokens: Mapped[int] = mapped_column(Integer, default=0)
    total_cost: Mapped[float] = mapped_column(Float, default=0.0)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, default="")

class ToolCall(Base):
    __tablename__ = "tool_calls"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    agent_run_id: Mapped[str] = mapped_column(String, ForeignKey("agent_runs.id"), nullable=True)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=False)
    tool_name: Mapped[str] = mapped_column(String(100), nullable=False)
    input: Mapped[dict] = mapped_column(JSON, default=dict)
    output: Mapped[dict] = mapped_column(JSON, default=dict)
    status: Mapped[str] = mapped_column(String(50), default="success")
    latency_ms: Mapped[int] = mapped_column(Integer, default=0)
    error_message: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Runbook(Base):
    __tablename__ = "runbooks"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"), nullable=False)
    service_id: Mapped[str] = mapped_column(String, ForeignKey("services.id"), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    content: Mapped[str] = mapped_column(Text, nullable=False)
    tags: Mapped[list] = mapped_column(JSON, default=list)
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class MemoryItem(Base):
    __tablename__ = "memory_items"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    team_id: Mapped[str] = mapped_column(String, ForeignKey("teams.id"), nullable=False)
    service_id: Mapped[str] = mapped_column(String, ForeignKey("services.id"), nullable=True)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=True)
    memory_type: Mapped[str] = mapped_column(String(100), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    importance_score: Mapped[float] = mapped_column(Float, default=0.5)
    confidence_score: Mapped[float] = mapped_column(Float, default=0.5)
    metadata_json: Mapped[dict] = mapped_column("metadata", JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ActionProposal(Base):
    __tablename__ = "action_proposals"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=False)
    agent_run_id: Mapped[str] = mapped_column(String, ForeignKey("agent_runs.id"), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    parameters: Mapped[dict] = mapped_column(JSON, default=dict)
    risk_level: Mapped[str] = mapped_column(String(50), default="medium")
    confidence_score: Mapped[float] = mapped_column(Float, default=0.0)
    requires_approval: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[str] = mapped_column(String(50), default="proposed")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    action_proposal_id: Mapped[str] = mapped_column(String, ForeignKey("action_proposals.id"), nullable=False)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=False)
    requested_to: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")
    decision_note: Mapped[str] = mapped_column(Text, default="")
    requested_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    decided_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

class ActionExecution(Base):
    __tablename__ = "action_executions"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    action_proposal_id: Mapped[str] = mapped_column(String, ForeignKey("action_proposals.id"), nullable=False)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=False)
    executor: Mapped[str] = mapped_column(String(100), default="deterministic_executor")
    status: Mapped[str] = mapped_column(String(50), default="running")
    input: Mapped[dict] = mapped_column(JSON, default=dict)
    output: Mapped[dict] = mapped_column(JSON, default=dict)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    error_message: Mapped[str] = mapped_column(Text, default="")

class Postmortem(Base):
    __tablename__ = "postmortems"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid_str)
    incident_id: Mapped[str] = mapped_column(String, ForeignKey("incidents.id"), nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[str] = mapped_column(Text, default="")
    impact: Mapped[str] = mapped_column(Text, default="")
    root_cause: Mapped[str] = mapped_column(Text, default="")
    timeline: Mapped[list] = mapped_column(JSON, default=list)
    resolution: Mapped[str] = mapped_column(Text, default="")
    prevention_items: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(50), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
