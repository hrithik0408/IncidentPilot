from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Runbook
from app.schemas import RunbookCreate
from app.services.demo_data import DEMO_TEAM_ID, ensure_demo_data

router = APIRouter()

@router.get("")
def list_runbooks(db: Session = Depends(get_db)):
    ensure_demo_data(db)
    return db.query(Runbook).all()

@router.post("")
def create_runbook(payload: RunbookCreate, db: Session = Depends(get_db)):
    rb = Runbook(team_id=DEMO_TEAM_ID, service_id=payload.service_id, title=payload.title, description=payload.description, content=payload.content, tags=payload.tags)
    db.add(rb)
    db.commit()
    db.refresh(rb)
    return rb

@router.post("/{runbook_id}/index")
def index_runbook(runbook_id: str):
    return {"runbook_id": runbook_id, "status": "indexed", "note": "MVP uses lightweight DB retrieval; vector indexing hook is ready."}
