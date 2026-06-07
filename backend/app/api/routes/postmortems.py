from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Postmortem

router = APIRouter()

@router.get("/{postmortem_id}")
def get_postmortem(postmortem_id: str, db: Session = Depends(get_db)):
    pm = db.get(Postmortem, postmortem_id)
    if not pm:
        raise HTTPException(status_code=404, detail="Postmortem not found")
    return pm
