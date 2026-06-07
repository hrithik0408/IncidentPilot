from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import ActionProposal, Approval, ActionExecution
from app.schemas import ApprovalRequest
from app.agents.supervisor import IncidentPilotSupervisor
from app.services.events import add_event

router = APIRouter()

@router.get("/{action_id}")
def get_action(action_id: str, db: Session = Depends(get_db)):
    action = db.get(ActionProposal, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return action

@router.post("/{action_id}/approve")
async def approve_action(action_id: str, payload: ApprovalRequest, db: Session = Depends(get_db)):
    action = db.get(ActionProposal, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    approval = db.query(Approval).filter_by(action_proposal_id=action_id, status="pending").first()
    if approval:
        approval.status = "approved"
        approval.decision_note = payload.decision_note
        approval.decided_at = datetime.utcnow()
    action.status = "approved"
    db.commit()
    add_event(db, action.incident_id, "action_approved", f"Approved: {action.title}", payload.decision_note, actor_type="human")
    result = await IncidentPilotSupervisor(db).execute_action(action_id)
    execution = db.query(ActionExecution).filter_by(action_proposal_id=action_id).order_by(ActionExecution.started_at.desc()).first()
    return {"status": "approved", "execution_id": execution.id if execution else None, "result": result}

@router.post("/{action_id}/reject")
def reject_action(action_id: str, payload: ApprovalRequest, db: Session = Depends(get_db)):
    action = db.get(ActionProposal, action_id)
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    approval = db.query(Approval).filter_by(action_proposal_id=action_id, status="pending").first()
    if approval:
        approval.status = "rejected"
        approval.decision_note = payload.decision_note
        approval.decided_at = datetime.utcnow()
    action.status = "rejected"
    db.commit()
    add_event(db, action.incident_id, "action_rejected", f"Rejected: {action.title}", payload.decision_note, actor_type="human")
    return {"status": "rejected"}
