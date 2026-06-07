from sqlalchemy.orm import Session
from app.models.models import IncidentEvent

def add_event(db: Session, incident_id: str, event_type: str, title: str, description: str = "", actor_type: str = "agent", data: dict | None = None):
    event = IncidentEvent(
        incident_id=incident_id,
        event_type=event_type,
        title=title,
        description=description,
        actor_type=actor_type,
        data=data or {},
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
