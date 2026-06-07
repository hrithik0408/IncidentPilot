from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import AgentRun, ToolCall

router = APIRouter()

@router.get("/{agent_run_id}")
def get_agent_run(agent_run_id: str, db: Session = Depends(get_db)):
    run = db.get(AgentRun, agent_run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Agent run not found")
    return run

@router.get("/{agent_run_id}/tool-calls")
def get_agent_tool_calls(agent_run_id: str, db: Session = Depends(get_db)):
    return db.query(ToolCall).filter_by(agent_run_id=agent_run_id).order_by(ToolCall.created_at.asc()).all()
