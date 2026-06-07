from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Incident, IncidentEvent, ActionProposal, ToolCall, AgentRun, Postmortem
from app.services.demo_data import ensure_demo_data
from app.agents.supervisor import IncidentPilotSupervisor
from app.schemas import AgentRunRequest

router = APIRouter()

@router.get("")
def list_incidents(db: Session = Depends(get_db)):
    ensure_demo_data(db)
    return db.query(Incident).order_by(Incident.created_at.desc()).all()

@router.get("/{incident_id}")
def get_incident(incident_id: str, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    action = db.query(ActionProposal).filter_by(incident_id=incident_id).order_by(ActionProposal.created_at.desc()).first()
    return {"incident": incident, "current_recommendation": action}

@router.get("/{incident_id}/events")
def get_events(incident_id: str, db: Session = Depends(get_db)):
    return db.query(IncidentEvent).filter_by(incident_id=incident_id).order_by(IncidentEvent.created_at.asc()).all()

@router.get("/{incident_id}/actions")
def get_actions(incident_id: str, db: Session = Depends(get_db)):
    return db.query(ActionProposal).filter_by(incident_id=incident_id).order_by(ActionProposal.created_at.desc()).all()

@router.get("/{incident_id}/tool-calls")
def get_tool_calls(incident_id: str, db: Session = Depends(get_db)):
    return db.query(ToolCall).filter_by(incident_id=incident_id).order_by(ToolCall.created_at.asc()).all()

@router.get("/{incident_id}/agent-runs")
def get_agent_runs(incident_id: str, db: Session = Depends(get_db)):
    return db.query(AgentRun).filter_by(incident_id=incident_id).order_by(AgentRun.started_at.desc()).all()

@router.post("/{incident_id}/agent/run")
async def run_agent(incident_id: str, payload: AgentRunRequest, db: Session = Depends(get_db)):
    supervisor = IncidentPilotSupervisor(db)
    return await supervisor.run_full_investigation(incident_id)

@router.get("/{incident_id}/postmortem")
def get_postmortem(incident_id: str, db: Session = Depends(get_db)):
    return db.query(Postmortem).filter_by(incident_id=incident_id).order_by(Postmortem.created_at.desc()).first()
