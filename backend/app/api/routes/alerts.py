from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Alert, Incident, Service
from app.schemas import AlertWebhook
from app.services.demo_data import DEMO_TEAM_ID, ensure_demo_data
from app.services.events import add_event
from app.agents.supervisor import IncidentPilotSupervisor

router = APIRouter()

@router.post("/webhook")
async def alert_webhook(payload: AlertWebhook, db: Session = Depends(get_db)):
    ensure_demo_data(db)
    service = db.query(Service).filter(Service.name == payload.service).first()
    incident = Incident(team_id=DEMO_TEAM_ID, service_id=service.id if service else None, title=payload.title, summary=payload.description, severity=payload.severity, status="open")
    db.add(incident)
    db.commit()
    db.refresh(incident)
    alert = Alert(team_id=DEMO_TEAM_ID, service_id=service.id if service else None, incident_id=incident.id, source=payload.source, external_alert_id=payload.external_alert_id, title=payload.title, description=payload.description, severity=payload.severity, payload=payload.model_dump())
    db.add(alert)
    db.commit()
    add_event(db, incident.id, "alert_received", f"Alert received from {payload.source}", payload.description, actor_type="system", data=payload.model_dump())
    supervisor = IncidentPilotSupervisor(db)
    result = await supervisor.run_full_investigation(incident.id)
    return {"alert_id": alert.id, "incident_id": incident.id, "status": "incident_created", "agent": result}
