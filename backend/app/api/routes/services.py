from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Service
from app.schemas import ServiceCreate
from app.services.demo_data import DEMO_TEAM_ID, ensure_demo_data

router = APIRouter()

@router.get("")
def list_services(db: Session = Depends(get_db)):
    ensure_demo_data(db)
    return db.query(Service).all()

@router.post("")
def create_service(payload: ServiceCreate, db: Session = Depends(get_db)):
    svc = Service(team_id=DEMO_TEAM_ID, name=payload.name, environment=payload.environment, description=payload.description, repository_url=payload.repository_url, healthcheck_url=payload.healthcheck_url, metadata_json=payload.metadata)
    db.add(svc)
    db.commit()
    db.refresh(svc)
    return svc
